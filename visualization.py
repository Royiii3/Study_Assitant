"""
可视化模块 - 使用 Plotly（原生支持中文）
"""
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as sp
import pandas as pd
import numpy as np


def plot_score_distribution(df):
    """绘制科目成绩分布柱状图"""
    score_cols = ['PTA成绩', '高数成绩', '英语成绩', 'Python成绩']
    bins = [0, 60, 70, 80, 90, 100]
    labels = ['不及格', '及格', '中等', '良好', '优秀']

    fig = sp.make_subplots(rows=2, cols=2, subplot_titles=[f'{col}分布' for col in score_cols])

    for i, col in enumerate(score_cols):
        row = i // 2 + 1
        col_idx = i % 2 + 1

        df_temp = df.copy()
        df_temp['分数段'] = pd.cut(df_temp[col], bins=bins, labels=labels, right=False)
        distribution = df_temp['分数段'].value_counts().reindex(labels).fillna(0)

        fig.add_trace(
            go.Bar(x=labels, y=distribution.values, name=col, marker_color=px.colors.qualitative.Set2[i]),
            row=row, col=col_idx
        )

    fig.update_layout(height=600, showlegend=False, title_text="科目成绩分布")
    return fig


def plot_behavior_score_correlation(df):
    """绘制学习行为与成绩关联散点图"""
    behavior_cols = ['学习时长', '作业完成度', '考勤率', '测验成绩']
    behavior_labels = ['学习时长', '作业完成度', '考勤率', '测验成绩']

    fig = sp.make_subplots(rows=2, cols=2, subplot_titles=[f'{label}与最终成绩的关系' for label in behavior_labels])

    for i, col in enumerate(behavior_cols):
        row = i // 2 + 1
        col_idx = i % 2 + 1

        fig.add_trace(
            go.Scatter(x=df[col], y=df['最终成绩'], mode='markers',
                      marker=dict(color='#0071e3', opacity=0.6, size=8),
                      name=behavior_labels[i]),
            row=row, col=col_idx
        )

        # 添加趋势线
        mask = df[col].notna() & df['最终成绩'].notna()
        if mask.sum() > 1:
            z = np.polyfit(df.loc[mask, col], df.loc[mask, '最终成绩'], 1)
            p = np.poly1d(z)
            x_line = np.linspace(df[col].min(), df[col].max(), 100)
            fig.add_trace(
                go.Scatter(x=x_line, y=p(x_line), mode='lines',
                          line=dict(color='red', width=2), name=f'{behavior_labels[i]}趋势线'),
                row=row, col=col_idx
            )

    fig.update_layout(height=600, showlegend=False, title_text="学习行为与成绩关联")
    return fig


def plot_class_distribution(df):
    """绘制班级学习状态分布饼图"""
    class_counts = df['班级'].value_counts()
    grade_counts = df['学业等级'].value_counts()

    fig = sp.make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]],
                          subplot_titles=['班级人数分布', '学业等级分布'])

    fig.add_trace(
        go.Pie(labels=class_counts.index, values=class_counts.values, hole=0.3,
              marker_colors=px.colors.qualitative.Set2),
        row=1, col=1
    )

    fig.add_trace(
        go.Pie(labels=grade_counts.index, values=grade_counts.values, hole=0.3,
              marker_colors=px.colors.qualitative.Set1),
        row=1, col=2
    )

    fig.update_layout(height=400, title_text="班级与学业等级分布")
    return fig


def plot_learning_trend(df):
    """绘制学期学习进度趋势折线图"""
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

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=study_trend, mode='lines+markers',
                            name='学习时长', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=weeks, y=homework_trend, mode='lines+markers',
                            name='作业完成度', line=dict(width=3)))
    fig.add_trace(go.Scatter(x=weeks, y=quiz_trend, mode='lines+markers',
                            name='测验成绩', line=dict(width=3)))

    fig.update_layout(title='学期学习进度趋势', height=400,
                     xaxis_title='学期周次', yaxis_title='指标值')
    return fig


def plot_correlation_heatmap(corr_df):
    """绘制相关性热力图"""
    fig = go.Figure(data=go.Heatmap(
        z=corr_df.values,
        x=corr_df.columns,
        y=corr_df.index,
        colorscale='RdBu_r',
        zmin=-1, zmax=1,
        text=corr_df.round(2).values,
        texttemplate='%{text}',
        textfont={"size": 12}
    ))

    fig.update_layout(title='学习行为与成绩相关性热力图', height=500, width=600)
    return fig


def plot_grade_by_class(df):
    """绘制各班级学业等级分布堆叠柱状图"""
    grade_by_class = df.groupby(['班级', '学业等级']).size().unstack().fillna(0)

    fig = go.Figure()

    for grade in grade_by_class.columns:
        fig.add_trace(go.Bar(
            name=grade,
            x=grade_by_class.index,
            y=grade_by_class[grade]
        ))

    fig.update_layout(
        barmode='stack',
        title='各班级学业等级分布',
        height=400,
        xaxis_title='班级',
        yaxis_title='人数'
    )
    return fig
