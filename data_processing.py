import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import os

def generate_synthetic_data():
    """
    生成符合真实规律的模拟大学生学习数据
    """
    np.random.seed(42)
    
    # 学生数量
    n_students = 200
    
    # 生成基础数据
    data = {
        '学号': ['202' + str(i).zfill(4) for i in range(1, n_students + 1)],
        '班级': np.random.choice(['金融1班', '金融2班', '金融3班', '金融4班'], n_students),
        '性别': np.random.choice(['男', '女'], n_students, p=[0.55, 0.45]),
        # 学习时长（每周小时数）
        '学习时长': np.random.normal(15, 5, n_students).clip(5, 35),
        # 作业完成度（百分比）
        '作业完成度': np.random.normal(85, 12, n_students).clip(40, 100),
        # 考勤率（百分比）
        '考勤率': np.random.normal(90, 8, n_students).clip(60, 100),
        # 测验成绩（百分制）
        '测验成绩': np.random.normal(75, 15, n_students).clip(30, 100),
        # 课堂参与度（1-5分）
        '课堂参与度': np.random.randint(1, 6, n_students),
        # 编程语言成绩
        '编程成绩': np.random.normal(78, 14, n_students).clip(40, 100),
        # 高等数学成绩
        '高数成绩': np.random.normal(72, 16, n_students).clip(35, 100),
        # 英语成绩
        '英语成绩': np.random.normal(75, 12, n_students).clip(40, 100),
        # Python语言成绩
        'Python成绩': np.random.normal(70, 15, n_students).clip(30, 100),
    }
    
    df = pd.DataFrame(data)
    
    # 计算最终成绩（综合所有因素）
    df['最终成绩'] = (df['编程成绩'] * 0.25 + df['高数成绩'] * 0.25 + 
                     df['英语成绩'] * 0.20 + df['Python成绩'] * 0.30).round(1)
    
    # 根据最终成绩划分学业等级
    def get_grade(score):
        if score >= 90:
            return '优'
        elif score >= 80:
            return '良'
        elif score >= 60:
            return '中'
        else:
            return '差'
    
    df['学业等级'] = df['最终成绩'].apply(get_grade)
    
    # 随机添加一些缺失值（模拟真实数据）
    # 每个字段最多5%的缺失值
    for col in ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度']:
        n_missing = int(n_students * 0.03)
        missing_indices = np.random.choice(df.index, n_missing, replace=False)
        df.loc[missing_indices, col] = np.nan
    
    # 随机添加一些异常值
    # 学习时长异常值
    n_outliers = int(n_students * 0.02)
    outlier_indices = np.random.choice(df.index, n_outliers, replace=False)
    df.loc[outlier_indices[:n_outliers//2], '学习时长'] = np.random.uniform(40, 60, n_outliers//2)
    df.loc[outlier_indices[n_outliers//2:], '学习时长'] = np.random.uniform(0, 3, n_outliers//2)
    
    return df

def load_data(file_path=None):
    """
    加载数据，如果没有提供文件路径或加载失败，则生成模拟数据
    """
    if file_path and os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            print(f"成功从文件加载数据: {file_path}")
            return df
        except Exception as e:
            print(f"加载文件失败: {e}，将生成模拟数据")
            return generate_synthetic_data()
    else:
        print("未提供数据文件，生成模拟数据")
        return generate_synthetic_data()

def handle_missing_values(df):
    """
    处理缺失值：数值型字段用均值填充，类别型字段用众数填充
    """
    df_copy = df.copy()
    
    # 数值型字段用均值填充
    numeric_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度',
                    '编程成绩', '高数成绩', '英语成绩', 'Python成绩', '最终成绩']
    
    for col in numeric_cols:
        if col in df_copy.columns:
            mean_val = df_copy[col].mean()
            df_copy[col] = df_copy[col].fillna(mean_val)
            print(f"填充 {col} 的缺失值，均值为: {mean_val:.2f}")
    
    # 类别型字段用众数填充
    categorical_cols = ['性别', '班级', '学业等级']
    for col in categorical_cols:
        if col in df_copy.columns:
            mode_val = df_copy[col].mode()[0]
            df_copy[col] = df_copy[col].fillna(mode_val)
            print(f"填充 {col} 的缺失值，众数为: {mode_val}")
    
    return df_copy

def handle_outliers(df):
    """
    处理异常值：使用IQR方法检测并替换为中位数
    """
    df_copy = df.copy()
    
    numeric_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩']
    
    for col in numeric_cols:
        if col not in df_copy.columns:
            continue
            
        Q1 = df_copy[col].quantile(0.25)
        Q3 = df_copy[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # 统计异常值数量
        outliers = (df_copy[col] < lower_bound) | (df_copy[col] > upper_bound)
        n_outliers = outliers.sum()
        
        if n_outliers > 0:
            median_val = df_copy[col].median()
            df_copy.loc[outliers, col] = median_val
            print(f"处理 {col} 的 {n_outliers} 个异常值，替换为中位数: {median_val:.2f}")
    
    return df_copy

def normalize_data(df):
    """
    标准化数据：对数值型特征进行标准化处理（Z-score标准化）
    """
    df_copy = df.copy()
    
    # 需要标准化的特征列
    feature_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度']
    
    scaler = StandardScaler()
    df_copy[feature_cols] = scaler.fit_transform(df_copy[feature_cols])
    
    return df_copy, scaler

def preprocess_data(df):
    """
    完整的数据预处理流程：处理缺失值 -> 处理异常值 -> 标准化
    """
    print("开始数据预处理...")
    
    # 处理缺失值
    df = handle_missing_values(df)
    
    # 处理异常值
    df = handle_outliers(df)
    
    # 标准化数据
    df, scaler = normalize_data(df)
    
    print("数据预处理完成")
    return df, scaler

def get_correlation_analysis(df):
    """
    计算学习行为与成绩的相关性分析
    """
    # 选择数值型列进行相关性分析
    numeric_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度', '最终成绩']
    corr_df = df[numeric_cols].corr()
    
    return corr_df

def get_class_statistics(df):
    """
    获取班级学习状态统计
    """
    class_stats = df.groupby('班级').agg({
        '学习时长': ['mean', 'std'],
        '作业完成度': ['mean', 'std'],
        '考勤率': ['mean', 'std'],
        '最终成绩': ['mean', 'std', 'count']
    }).round(2)
    
    # 重命名列索引为中文
    class_stats.columns = [
        ('学习时长', '平均值'), ('学习时长', '标准差'),
        ('作业完成度', '平均值'), ('作业完成度', '标准差'),
        ('考勤率', '平均值'), ('考勤率', '标准差'),
        ('最终成绩', '平均值'), ('最终成绩', '标准差'), ('最终成绩', '人数')
    ]
    
    return class_stats

def get_grade_distribution(df):
    """
    获取学业等级分布统计
    """
    grade_dist = df['学业等级'].value_counts(normalize=True).sort_index()
    grade_dist = grade_dist.rename('比例')
    return grade_dist