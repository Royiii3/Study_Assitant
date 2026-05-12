"""
预测模块
提供模型训练和预测功能
"""
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from config import BEHAVIOR_FEATURES, MODEL_CONFIG


def train_prediction_model(df):
    """训练逻辑回归预测模型"""
    feature_cols = BEHAVIOR_FEATURES
    target_col = '学业等级'

    X = df[feature_cols].copy()
    y = df[target_col]

    # 处理缺失值
    if X.isnull().any().any():
        for col in feature_cols:
            if X[col].isnull().any():
                X[col] = X[col].fillna(X[col].mean())

    # 对目标变量进行编码
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded,
        test_size=MODEL_CONFIG['test_size'],
        random_state=MODEL_CONFIG['random_state']
    )

    # 训练模型
    model = LogisticRegression(
        solver=MODEL_CONFIG['solver'],
        max_iter=MODEL_CONFIG['max_iter'],
        random_state=MODEL_CONFIG['random_state']
    )
    model.fit(X_train, y_train)

    # 预测
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # 计算准确率
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)

    # 生成分类报告
    unique_labels = np.unique(np.concatenate([y_test, y_test_pred]))
    class_names = label_encoder.classes_
    existing_class_names = [class_names[i] for i in unique_labels]

    class_report = "=" * 60 + "\n"
    class_report += "                    分类报告\n"
    class_report += "=" * 60 + "\n"
    class_report += f"{'类别':<8} {'精确率':<8} {'召回率':<8} {'F1分数':<8} {'支持数':<8}\n"
    class_report += "-" * 60 + "\n"

    all_precisions = []
    all_recalls = []
    all_f1s = []
    total_support = 0

    for i, class_name in enumerate(existing_class_names):
        label = unique_labels[i]
        tp = np.sum((y_test == label) & (y_test_pred == label))
        fp = np.sum((y_test != label) & (y_test_pred == label))
        fn = np.sum((y_test == label) & (y_test_pred != label))
        support = np.sum(y_test == label)

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

        all_precisions.append(precision)
        all_recalls.append(recall)
        all_f1s.append(f1)
        total_support += support

        class_report += f"{class_name:<8} {precision:<8.2f} {recall:<8.2f} {f1:<8.2f} {support:<8}\n"

    class_report += "-" * 60 + "\n"

    # 计算总体指标
    total_samples = len(y_test)
    correct_predictions = np.sum(y_test == y_test_pred)
    accuracy = correct_predictions / total_samples if total_samples > 0 else 0.0

    macro_precision = np.mean(all_precisions)
    macro_recall = np.mean(all_recalls)
    macro_f1 = np.mean(all_f1s)

    weighted_precision = np.average(all_precisions, weights=[np.sum(y_test == l) for l in unique_labels])
    weighted_recall = np.average(all_recalls, weights=[np.sum(y_test == l) for l in unique_labels])
    weighted_f1 = np.average(all_f1s, weights=[np.sum(y_test == l) for l in unique_labels])

    class_report += f"{'准确率':<8} {'':<8} {'':<8} {'':<8} {accuracy:<8.2f}\n"
    class_report += f"{'宏平均':<8} {macro_precision:<8.2f} {macro_recall:<8.2f} {macro_f1:<8.2f} {total_support:<8}\n"
    class_report += f"{'加权平均':<8} {weighted_precision:<8.2f} {weighted_recall:<8.2f} {weighted_f1:<8.2f} {total_support:<8}\n"
    class_report += "=" * 60 + "\n"

    # 混淆矩阵
    conf_matrix = confusion_matrix(y_test, y_test_pred, labels=unique_labels)

    return model, label_encoder, {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'class_report': class_report,
        'conf_matrix': conf_matrix,
        'classes': existing_class_names
    }


def predict_grade(model, label_encoder, scaler, input_data):
    """使用训练好的模型进行预测"""
    feature_cols = BEHAVIOR_FEATURES

    input_df = pd.DataFrame([input_data])

    # 标准化输入数据
    input_df[feature_cols] = scaler.transform(input_df[feature_cols])

    # 预测
    prediction_encoded = model.predict(input_df[feature_cols])
    prediction = label_encoder.inverse_transform(prediction_encoded)[0]

    # 计算概率
    probabilities = model.predict_proba(input_df[feature_cols])[0]
    prob_dict = dict(zip(label_encoder.classes_, probabilities))

    return prediction, prob_dict
