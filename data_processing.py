"""
数据处理模块
提供数据加载、预处理、统计分析功能
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from config import (
    BEHAVIOR_FEATURES, SUBJECT_SCORES, SUBJECT_WEIGHTS,
    GRADE_THRESHOLDS, CLASSES, SYNTHETIC_DATA_CONFIG
)


def generate_synthetic_data():
    """生成符合真实规律的模拟大学生学习数据"""
    cfg = SYNTHETIC_DATA_CONFIG
    np.random.seed(cfg['random_seed'])
    n = cfg['n_students']

    data = {
        '学号': ['202' + str(i).zfill(4) for i in range(1, n + 1)],
        '班级': np.random.choice(CLASSES, n),
        '性别': np.random.choice(['男', '女'], n, p=[0.55, 0.45]),
        '学习时长': np.random.normal(15, 5, n).clip(5, 35),
        '作业完成度': np.random.normal(85, 12, n).clip(40, 100),
        '考勤率': np.random.normal(90, 8, n).clip(60, 100),
        '测验成绩': np.random.normal(75, 15, n).clip(30, 100),
        '课堂参与度': np.random.randint(1, 6, n),
        '编程成绩': np.random.normal(78, 14, n).clip(40, 100),
        '高数成绩': np.random.normal(72, 16, n).clip(35, 100),
        '英语成绩': np.random.normal(75, 12, n).clip(40, 100),
        'Python成绩': np.random.normal(70, 15, n).clip(30, 100),
    }

    df = pd.DataFrame(data)

    # 计算最终成绩
    df['最终成绩'] = sum(df[col] * weight for col, weight in SUBJECT_WEIGHTS.items()).round(1)

    # 划分学业等级
    def get_grade(score):
        for threshold, grade in GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return '差'

    df['学业等级'] = df['最终成绩'].apply(get_grade)

    # 添加缺失值
    n_missing = int(n * cfg['missing_rate'])
    for col in BEHAVIOR_FEATURES:
        missing_indices = np.random.choice(df.index, n_missing, replace=False)
        df.loc[missing_indices, col] = np.nan

    # 添加异常值
    n_outliers = int(n * cfg['outlier_rate'])
    outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
    df.loc[outlier_indices[:n_outliers//2], '学习时长'] = np.random.uniform(40, 60, n_outliers//2)
    df.loc[outlier_indices[n_outliers//2:], '学习时长'] = np.random.uniform(0, 3, n_outliers//2)

    return df


def load_data(file_path=None):
    """加载数据，如果没有提供文件路径则生成模拟数据"""
    if file_path:
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception:
            return generate_synthetic_data()
    return generate_synthetic_data()


def handle_missing_values(df):
    """处理缺失值：数值型用均值填充，类别型用众数填充"""
    df_copy = df.copy()

    numeric_cols = BEHAVIOR_FEATURES + SUBJECT_SCORES + ['最终成绩']
    for col in numeric_cols:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].fillna(df_copy[col].mean())

    categorical_cols = ['性别', '班级', '学业等级']
    for col in categorical_cols:
        if col in df_copy.columns:
            df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])

    return df_copy


def handle_outliers(df):
    """处理异常值：使用IQR方法检测并替换为中位数"""
    df_copy = df.copy()

    for col in BEHAVIOR_FEATURES:
        if col not in df_copy.columns:
            continue

        Q1 = df_copy[col].quantile(0.25)
        Q3 = df_copy[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = (df_copy[col] < lower_bound) | (df_copy[col] > upper_bound)
        if outliers.sum() > 0:
            df_copy.loc[outliers, col] = df_copy[col].median()

    return df_copy


def normalize_data(df):
    """标准化数据：Z-score标准化"""
    df_copy = df.copy()
    scaler = StandardScaler()
    df_copy[BEHAVIOR_FEATURES] = scaler.fit_transform(df_copy[BEHAVIOR_FEATURES])
    return df_copy, scaler


def preprocess_data(df):
    """完整的数据预处理流程"""
    df = handle_missing_values(df)
    df = handle_outliers(df)
    df, scaler = normalize_data(df)
    return df, scaler


def get_correlation_analysis(df):
    """计算学习行为与成绩的相关性分析"""
    numeric_cols = BEHAVIOR_FEATURES + ['最终成绩']
    return df[numeric_cols].corr()


def get_class_statistics(df):
    """获取班级学习状态统计"""
    class_stats = df.groupby('班级').agg({
        '学习时长': ['mean', 'std'],
        '作业完成度': ['mean', 'std'],
        '考勤率': ['mean', 'std'],
        '最终成绩': ['mean', 'std', 'count']
    }).round(2)

    class_stats.columns = [
        ('学习时长', '平均值'), ('学习时长', '标准差'),
        ('作业完成度', '平均值'), ('作业完成度', '标准差'),
        ('考勤率', '平均值'), ('考勤率', '标准差'),
        ('最终成绩', '平均值'), ('最终成绩', '标准差'), ('最终成绩', '人数')
    ]

    return class_stats


def get_grade_distribution(df):
    """获取学业等级分布统计"""
    grade_dist = df['学业等级'].value_counts(normalize=True).sort_index()
    return grade_dist.rename('比例')
