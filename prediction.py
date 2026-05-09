from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np

def train_prediction_model(df):
    """
    训练逻辑回归预测模型
    """
    # 选择特征和目标变量
    feature_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度']
    target_col = '学业等级'
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 检查并处理缺失值（确保数据完整性）
    if X.isnull().any().any():
        print("检测到缺失值，正在填充...")
        for col in feature_cols:
            if X[col].isnull().any():
                mean_val = X[col].mean()
                X[col] = X[col].fillna(mean_val)
    
    # 对目标变量进行编码
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # 划分训练集和测试集（80%训练，20%测试）
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, 
                                                        test_size=0.2, 
                                                        random_state=42)
    
    # 创建并训练逻辑回归模型
    model = LogisticRegression(solver='lbfgs', 
                               max_iter=200,
                               random_state=42)
    model.fit(X_train, y_train)
    
    # 在训练集和测试集上进行预测
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)
    
    # 计算准确率
    train_accuracy = accuracy_score(y_train, y_train_pred)
    test_accuracy = accuracy_score(y_test, y_test_pred)
    
    # 生成分类报告（确保标签匹配）
    # 先找出实际出现在测试集和预测结果中的标签
    unique_labels = np.unique(np.concatenate([y_test, y_test_pred]))
    class_names = label_encoder.classes_
    # 只保留存在的类别名称
    existing_class_names = [class_names[i] for i in unique_labels]
    
    # 生成完全中文的分类报告
    class_report = "=" * 60 + "\n"
    class_report += "                    分类报告\n"
    class_report += "=" * 60 + "\n"
    class_report += f"{'类别':<8} {'精确率':<8} {'召回率':<8} {'F1分数':<8} {'支持数':<8}\n"
    class_report += "-" * 60 + "\n"
    
    # 计算每个类别的指标
    for i, class_name in enumerate(existing_class_names):
        label = unique_labels[i]
        # 计算精确率
        tp = np.sum((y_test == label) & (y_test_pred == label))
        fp = np.sum((y_test != label) & (y_test_pred == label))
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        
        # 计算召回率
        fn = np.sum((y_test == label) & (y_test_pred != label))
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        
        # 计算F1分数
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        
        # 支持数
        support = np.sum(y_test == label)
        
        class_report += f"{class_name:<8} {precision:<8.2f} {recall:<8.2f} {f1:<8.2f} {support:<8}\n"
    
    class_report += "-" * 60 + "\n"
    
    # 计算总体指标
    total_samples = len(y_test)
    correct_predictions = np.sum(y_test == y_test_pred)
    accuracy = correct_predictions / total_samples if total_samples > 0 else 0.0
    
    # 宏平均
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
    
    macro_precision = np.mean(all_precisions)
    macro_recall = np.mean(all_recalls)
    macro_f1 = np.mean(all_f1s)
    
    # 加权平均
    weighted_precision = np.average(all_precisions, weights=[np.sum(y_test == l) for l in unique_labels])
    weighted_recall = np.average(all_recalls, weights=[np.sum(y_test == l) for l in unique_labels])
    weighted_f1 = np.average(all_f1s, weights=[np.sum(y_test == l) for l in unique_labels])
    
    class_report += f"{'准确率':<8} {'':<8} {'':<8} {'':<8} {accuracy:<8.2f}\n"
    class_report += f"{'宏平均':<8} {macro_precision:<8.2f} {macro_recall:<8.2f} {macro_f1:<8.2f} {total_support:<8}\n"
    class_report += f"{'加权平均':<8} {weighted_precision:<8.2f} {weighted_recall:<8.2f} {weighted_f1:<8.2f} {total_support:<8}\n"
    class_report += "=" * 60 + "\n"
    
    # 生成混淆矩阵
    conf_matrix = confusion_matrix(y_test, y_test_pred, labels=unique_labels)
    
    print(f"模型训练完成！")
    print(f"训练集准确率: {train_accuracy:.2f}")
    print(f"测试集准确率: {test_accuracy:.2f}")
    
    return model, label_encoder, {
        'train_accuracy': train_accuracy,
        'test_accuracy': test_accuracy,
        'class_report': class_report,
        'conf_matrix': conf_matrix,
        'classes': existing_class_names
    }

def predict_grade(model, label_encoder, scaler, input_data):
    """
    使用训练好的模型进行预测
    参数：
        model: 训练好的模型
        label_encoder: 标签编码器
        scaler: 数据标准化器
        input_data: 用户输入的学习行为数据（字典形式）
    """
    # 将输入数据转换为DataFrame
    input_df = pd.DataFrame([input_data])
    
    # 需要标准化的特征列
    feature_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度']
    
    # 对输入数据进行标准化
    input_df[feature_cols] = scaler.transform(input_df[feature_cols])
    
    # 进行预测
    prediction_encoded = model.predict(input_df[feature_cols])
    
    # 将编码转换为原始标签
    prediction = label_encoder.inverse_transform(prediction_encoded)[0]
    
    # 计算预测概率
    probabilities = model.predict_proba(input_df[feature_cols])[0]
    prob_dict = dict(zip(label_encoder.classes_, probabilities))
    
    return prediction, prob_dict

def get_model_metrics(model, label_encoder, X_test, y_test):
    """
    获取模型评估指标
    """
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    class_report = classification_report(y_test, y_pred, 
                                         target_names=label_encoder.classes_)
    conf_matrix = confusion_matrix(y_test, y_pred)
    
    return {
        'accuracy': accuracy,
        'class_report': class_report,
        'conf_matrix': conf_matrix
    }

def prepare_training_data(df):
    """
    准备训练数据：分离特征和标签
    """
    feature_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度']
    target_col = '学业等级'
    
    X = df[feature_cols]
    y = df[target_col]
    
    # 对目标变量进行编码
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # 划分训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, 
                                                        test_size=0.2, 
                                                        random_state=42)
    
    return X_train, X_test, y_train, y_test, label_encoder