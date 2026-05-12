"""
学习行为数据分析与学业预测系统
主入口文件
"""
import streamlit as st
from config import PAGE_CONFIG
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_feature_grid, render_steps
)

# 页面配置
st.set_page_config(**PAGE_CONFIG)

# 加载样式
load_custom_css()

# 渲染侧边栏
render_sidebar()

# Hero 区域 - Apple 风格
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title fade-in">学习行为分析<br>与学业预测</h1>
    <p class="hero-subtitle fade-in">
        基于机器学习技术，深入分析学生学习行为数据，<br>智能预测学业等级，助力教育决策。
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 功能介绍 - Apple 风格网格
features = [
    (" ", "数据加载", "上传CSV文件或生成模拟数据，开始分析之旅"),
    ("⚙️", "数据预处理", "智能处理缺失值、异常值，标准化数据格式"),
    (" ", "统计分析", "深入分析学习行为与成绩的相关性"),
    (" ", "可视化展示", "多维度图表，直观呈现数据特征"),
    (" ", "学业预测", "基于逻辑回归模型，智能预测学业等级"),
    (" ", "模型评估", "准确率、混淆矩阵，全面评估模型性能"),
]
render_feature_grid(features)

st.markdown("<br><br>", unsafe_allow_html=True)

# 使用说明 - Apple 风格步骤
st.markdown("""
<div class="custom-card">
    <h3>快速开始</h3>
    <p>按照以下步骤，开始您的数据分析之旅</p>
</div>
""", unsafe_allow_html=True)

steps = [
    '前往「数据加载」页面，上传CSV文件或点击「生成模拟数据」',
    '进入「数据预处理」页面，点击「执行预处理」清洗数据',
    '在「统计分析」页面查看相关性和分布统计',
    '通过「可视化展示」页面查看各类图表分析',
    '前往「学业预测」页面训练模型并预测学业等级',
    '最后在「模型评估」页面查看模型性能指标',
]
render_steps(steps)

st.markdown("<br><br>", unsafe_allow_html=True)

# 数据格式说明 - Apple 风格
st.markdown("""
<div class="custom-card">
    <h3>数据格式</h3>
    <p>CSV文件应包含以下字段</p>
    <div style="margin-top: 1.5rem;">
        <table style="width: 100%; border-collapse: collapse;">
            <tr style="border-bottom: 1px solid #e8e8ed;">
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">学号</td>
                <td style="padding: 0.75rem 0; color: #86868b;">学生编号</td>
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">班级</td>
                <td style="padding: 0.75rem 0; color: #86868b;">所在班级</td>
            </tr>
            <tr style="border-bottom: 1px solid #e8e8ed;">
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">学习时长</td>
                <td style="padding: 0.75rem 0; color: #86868b;">每周学习时长（小时）</td>
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">作业完成度</td>
                <td style="padding: 0.75rem 0; color: #86868b;">作业完成百分比</td>
            </tr>
            <tr style="border-bottom: 1px solid #e8e8ed;">
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">考勤率</td>
                <td style="padding: 0.75rem 0; color: #86868b;">考勤百分比</td>
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">测验成绩</td>
                <td style="padding: 0.75rem 0; color: #86868b;">最近测验成绩</td>
            </tr>
            <tr>
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">课堂参与度</td>
                <td style="padding: 0.75rem 0; color: #86868b;">1-5分</td>
                <td style="padding: 0.75rem 0; font-weight: 600; color: #1d1d1f;">各科成绩</td>
                <td style="padding: 0.75rem 0; color: #86868b;">编程/高数/英语/Python</td>
            </tr>
        </table>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 技术栈 - Apple 风格
st.markdown("""
<div class="custom-card" style="text-align: center;">
    <h3>技术栈</h3>
    <p style="margin-top: 1rem;">
        Streamlit · scikit-learn · pandas · matplotlib · seaborn
    </p>
</div>
""", unsafe_allow_html=True)

# 页脚
render_footer()
