"""
大学生学习行为数据分析与学业预测系统
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

# 主页内容
st.markdown("""
<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; margin: 0; font-size: 2.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        大学生学习行为数据分析与学业预测系统
    </h1>
    <p style="text-align: center; color: #6c757d; font-size: 1.1rem; margin-top: 0.5rem;">
        基于机器学习的学习行为分析与学业等级预测平台
    </p>
</div>
""", unsafe_allow_html=True)

# 功能介绍
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>  数据加载</h3>
        <p style="color: #6c757d;">上传CSV文件或生成模拟数据，开始分析之旅</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>⚙️ 数据预处理</h3>
        <p style="color: #6c757d;">自动处理缺失值、异常值，标准化数据格式</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>  统计分析</h3>
        <p style="color: #6c757d;">深入分析学习行为与成绩的相关性</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>  可视化展示</h3>
        <p style="color: #6c757d;">多维度图表，直观呈现数据特征</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>  学业预测</h3>
        <p style="color: #6c757d;">基于逻辑回归模型，预测学业等级</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="custom-card" style="text-align: center;">
        <h3>  模型评估</h3>
        <p style="color: #6c757d;">准确率、混淆矩阵，全面评估模型性能</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 使用说明
st.markdown("""
<div class="custom-card">
    <h3 style="margin-top: 0;">  使用说明</h3>
    <ol style="color: #6c757d; line-height: 2;">
        <li>点击左侧 <strong>  数据加载</strong> 上传CSV文件或生成模拟数据</li>
        <li>进入 <strong>⚙️ 数据预处理</strong> 执行数据清洗和标准化</li>
        <li>在 <strong>  统计分析</strong> 查看相关性和分布统计</li>
        <li>通过 <strong>  可视化展示</strong> 查看各类图表</li>
        <li>在 <strong>  学业预测</strong> 训练模型并预测学业等级</li>
        <li>最后在 <strong>  模型评估</strong> 查看模型性能指标</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# 数据格式说明
st.markdown("""
<div class="custom-card">
    <h3 style="margin-top: 0;">  数据格式</h3>
    <p style="color: #6c757d;">CSV文件应包含以下字段：</p>
    <table style="width: 100%; color: #6c757d;">
        <tr><td><strong>学号</strong></td><td>学生编号</td><td><strong>班级</strong></td><td>所在班级</td></tr>
        <tr><td><strong>学习时长</strong></td><td>每周学习时长（小时）</td><td><strong>作业完成度</strong></td><td>作业完成百分比</td></tr>
        <tr><td><strong>考勤率</strong></td><td>考勤百分比</td><td><strong>测验成绩</strong></td><td>最近测验成绩</td></tr>
        <tr><td><strong>课堂参与度</strong></td><td>1-5分</td><td><strong>各科成绩</strong></td><td>编程/高数/英语/Python</td></tr>
    </table>
</div>
""", unsafe_allow_html=True)

# 技术栈
st.markdown("""
<div class="custom-card">
    <h3 style="margin-top: 0;">  技术栈</h3>
    <p style="color: #6c757d;">
        <strong>前端框架：</strong>Streamlit |
        <strong>数据分析：</strong>pandas, numpy |
        <strong>可视化：</strong>matplotlib, seaborn |
        <strong>机器学习：</strong>scikit-learn（逻辑回归）
    </p>
</div>
""", unsafe_allow_html=True)

# 页脚
render_footer()
