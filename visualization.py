"""
可视化模块
提供各种图表绘制功能
"""
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import pandas as pd


def setup_font():
    """设置中文字体 - 兼容 Linux/Windows/Mac"""
    import platform
    system = platform.system()

    if system == "Windows":
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    elif system == "Darwin":  # Mac
        plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang SC', 'DejaVu Sans']
    else:  # Linux
        plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'Noto Sans CJK SC', 'DejaVu Sans']

    plt.rcParams['axes.unicode_minus'] = False

    # 如果上述字体都不可用，使用 matplotlib 内置的方式
    try:
        matplotlib.font_manager.findfont('DejaVu Sans')
    except:
        pass


def plot_score_distribution(df):
    """绘制科目成绩分布柱状图"""
    setup_font()

    score_cols = ['编程成绩', '高数成绩', '英语成绩', 'Python成绩']
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    bins = [0, 60, 70, 80, 90, 100]
    labels = ['不及格', '及格', '中等', '良好', '优秀']

    for i, col in enumerate(score_cols):
        ax = axes[i]
        df['分数段'] = pd.cut(df[col], bins=bins, labels=labels, right=False)
        distribution = df['分数段'].value_counts().reindex(labels)

        sns.barplot(x=distribution.index, y=distribution.values, ax=ax,
                    palette='viridis', alpha=0.8)

        ax.set_title(f'{col}分布', fontsize=12)
        ax.set_xlabel('分数段', fontsize=10)
        ax.set_ylabel('人数', fontsize=10)
        ax.tick_params(axis='x', rotation=30)

        for p in ax.patches:
            height = p.get_height()
            ax.text(p.get_x() + p.get_width()/2., height,
                    f'{int(height)}', ha='center', va='bottom')

    plt.tight_layout()
    return fig


def plot_behavior_score_correlation(df):
    """绘制学习行为与成绩关联散点图"""
    setup_font()

    behavior_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩']
    behavior_labels = ['学习时长', '作业完成度', '考勤率', '测验成绩']

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()

    for i, col in enumerate(behavior_cols):
        ax = axes[i]
        sns.regplot(x=df[col], y=df['最终成绩'], ax=ax,
                    scatter_kws={'alpha': 0.6, 's': 40},
                    line_kws={'color': 'red', 'linewidth': 2})

        ax.set_title(f'{behavior_labels[i]}与最终成绩的关系', fontsize=12)
        ax.set_xlabel(behavior_labels[i], fontsize=10)
        ax.set_ylabel('最终成绩', fontsize=10)

    plt.tight_layout()
    return fig


def plot_class_distribution(df):
    """绘制班级学习状态分布饼图"""
    setup_font()

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # 班级人数分布
    class_counts = df['班级'].value_counts()
    axes[0].pie(class_counts.values, labels=class_counts.index,
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set2'))
    axes[0].set_title('班级人数分布', fontsize=12)

    # 学业等级分布
    grade_counts = df['学业等级'].value_counts()
    axes[1].pie(grade_counts.values, labels=grade_counts.index,
                autopct='%1.1f%%', startangle=90, colors=sns.color_palette('Set1'))
    axes[1].set_title('学业等级分布', fontsize=12)

    plt.tight_layout()
    return fig


def plot_learning_trend(df):
    """绘制学期学习进度趋势折线图"""
    setup_font()

    weeks = ['第1周', '第4周', '第8周', '第12周', '第16周']

    study_trend = [df['学习时长'].mean() - 2, df['学习时长'].mean() - 1,
                   df['学习时长'].mean(), df['学习时长'].mean() + 1,
                   df['学习时长'].mean() + 2]

    homework_trend = [df['作业完成度'].mean() - 5, df['作业完成度'].mean() - 2,
                      df['作业完成度'].mean(), df['作业完成度'].mean() + 2,
                      df['作业完成度'].mean() + 3]

    quiz_trend = [df['测验成绩'].mean() - 8, df['测验成绩'].mean() - 3,
                  df['测验成绩'].mean(), df['测验成绩'].mean() + 3,
                  df['测验成绩'].mean() + 5]

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(weeks, study_trend, marker='o', label='学习时长', linewidth=2, color='blue')
    ax.plot(weeks, homework_trend, marker='s', label='作业完成度', linewidth=2, color='green')
    ax.plot(weeks, quiz_trend, marker='^', label='测验成绩', linewidth=2, color='orange')

    ax.set_title('学期学习进度趋势', fontsize=14)
    ax.set_xlabel('学期周次', fontsize=12)
    ax.set_ylabel('指标值', fontsize=12)
    ax.legend(fontsize=12)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    return fig


def plot_correlation_heatmap(corr_df):
    """绘制相关性热力图"""
    setup_font()

    fig, ax = plt.subplots(figsize=(10, 8))

    sns.heatmap(corr_df, annot=True, cmap='coolwarm', ax=ax,
                fmt='.2f', linewidths=0.5, vmin=-1, vmax=1)

    ax.set_title('学习行为与成绩相关性热力图', fontsize=14)

    plt.tight_layout()
    return fig


def plot_grade_by_class(df):
    """绘制各班级学业等级分布堆叠柱状图"""
    setup_font()

    grade_by_class = df.groupby(['班级', '学业等级']).size().unstack().fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))

    grade_by_class.plot(kind='bar', stacked=True, ax=ax,
                        color=sns.color_palette('Set1'), alpha=0.8)

    ax.set_title('各班级学业等级分布', fontsize=14)
    ax.set_xlabel('班级', fontsize=12)
    ax.set_ylabel('人数', fontsize=12)
    ax.legend(title='学业等级', fontsize=10)
    ax.tick_params(axis='x', rotation=30)

    plt.tight_layout()
    return fig
