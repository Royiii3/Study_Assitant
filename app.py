"""
学习行为数据分析与学业预测系统
主入口文件
"""
import streamlit as st
from config import PAGE_CONFIG
from utils import load_custom_css, render_sidebar, render_footer

# 页面配置
st.set_page_config(**PAGE_CONFIG)

# 加载样式
load_custom_css()

# 渲染侧边栏
render_sidebar()

# Hero 区域
st.markdown('<div class="hero-section">', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title fade-in">学习行为分析<br>与学业预测</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-subtitle fade-in">基于机器学习技术，深入分析学生学习行为数据，<br>智能预测学业等级，助力教育决策。</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 功能介绍 - 使用 Streamlit 原生列
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon"> </div>
        <div class="feature-title">数据加载</div>
        <div class="feature-desc">上传CSV文件或生成模拟数据</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon">⚙️</div>
        <div class="feature-title">数据预处理</div>
        <div class="feature-desc">处理缺失值、异常值，标准化数据</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon"> </div>
        <div class="feature-title">统计分析</div>
        <div class="feature-desc">分析学习行为与成绩的相关性</div>
    </div>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon"> </div>
        <div class="feature-title">可视化展示</div>
        <div class="feature-desc">多维度图表，直观呈现数据</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon"> </div>
        <div class="feature-title">学业预测</div>
        <div class="feature-desc">基于逻辑回归模型预测学业等级</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-item">
        <div class="feature-icon"> </div>
        <div class="feature-title">模型评估</div>
        <div class="feature-desc">准确率、混淆矩阵评估模型</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 使用说明
st.markdown("""
<div class="custom-card">
    <h3>快速开始</h3>
    <p>按照以下步骤，开始您的数据分析之旅</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<ol class="steps-list">
    <li>前往「数据加载」页面，上传CSV文件或点击「生成模拟数据」</li>
    <li>进入「数据预处理」页面，点击「执行预处理」清洗数据</li>
    <li>在「统计分析」页面查看相关性和分布统计</li>
    <li>通过「可视化展示」页面查看各类图表分析</li>
    <li>前往「学业预测」页面训练模型并预测学业等级</li>
    <li>最后在「模型评估」页面查看模型性能指标</li>
</ol>
""", unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 数据格式说明
st.markdown("""
<div class="custom-card">
    <h3>数据格式</h3>
    <p>CSV文件应包含以下字段</p>
</div>
""", unsafe_allow_html=True)

# 使用 Streamlit 原生表格
import pandas as pd
format_df = pd.DataFrame({
    '字段': ['学号', '班级', '学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度', '各科成绩'],
    '说明': ['学生编号', '所在班级', '每周学习时长（小时）', '作业完成百分比', '考勤百分比', '最近测验成绩', '1-5分', '编程/高数/英语/Python']
})
st.dataframe(format_df, use_container_width=True, hide_index=True)

st.markdown("<br>", unsafe_allow_html=True)

# 技术栈
st.markdown("""
<div class="custom-card" style="text-align: center;">
    <h3>技术栈</h3>
    <p style="margin-top: 1rem;">Streamlit · scikit-learn · pandas · matplotlib · seaborn</p>
</div>
""", unsafe_allow_html=True)

# 页脚
render_footer()
