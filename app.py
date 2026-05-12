"""
学习行为数据分析与学业预测系统
主入口文件 - 使用 streamlit-shadcn-ui
"""
import streamlit as st
import streamlit_shadcn_ui as ui
from config import PAGE_CONFIG
from utils import load_custom_css, render_sidebar, render_footer

# 页面配置
st.set_page_config(**PAGE_CONFIG)

# 加载样式
load_custom_css()

# 渲染侧边栏
render_sidebar()

# Hero 区域 - 使用 shadcn 样式
st.markdown("""
<div style="text-align: center; padding: 4rem 2rem 3rem;">
    <h1 style="font-size: 3rem; font-weight: 700; letter-spacing: -0.03em; line-height: 1.1; margin-bottom: 1rem; color: #0f172a;">
        学习行为分析与学业预测
    </h1>
    <p style="font-size: 1.25rem; color: #64748b; max-width: 600px; margin: 0 auto; line-height: 1.6;">
        基于机器学习技术，深入分析学生学习行为数据，智能预测学业等级
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 功能卡片 - 使用 shadcn Card
col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with ui.card(key="card1"):
        st.markdown("###   数据加载")
        st.markdown("上传CSV文件或生成模拟数据")

with col2:
    with ui.card(key="card2"):
        st.markdown("### ⚙️ 数据预处理")
        st.markdown("处理缺失值、异常值，标准化数据")

with col3:
    with ui.card(key="card3"):
        st.markdown("###   统计分析")
        st.markdown("分析学习行为与成绩的相关性")

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    with ui.card(key="card4"):
        st.markdown("###   可视化展示")
        st.markdown("多维度图表，直观呈现数据")

with col2:
    with ui.card(key="card5"):
        st.markdown("###   学业预测")
        st.markdown("基于逻辑回归模型预测学业等级")

with col3:
    with ui.card(key="card6"):
        st.markdown("###   模型评估")
        st.markdown("准确率、混淆矩阵评估模型")

st.markdown("<br><br>", unsafe_allow_html=True)

# 使用说明 - 使用 shadcn 样式
with ui.card(key="steps_card"):
    st.markdown("### 快速开始")
    st.markdown("按照以下步骤，开始您的数据分析之旅")
    st.markdown("""
    1. 前往「数据加载」页面，上传CSV文件或点击「生成模拟数据」
    2. 进入「数据预处理」页面，点击「执行预处理」清洗数据
    3. 在「统计分析」页面查看相关性和分布统计
    4. 通过「可视化展示」页面查看各类图表分析
    5. 前往「学业预测」页面训练模型并预测学业等级
    6. 最后在「模型评估」页面查看模型性能指标
    """)

st.markdown("<br>", unsafe_allow_html=True)

# 数据格式说明
with ui.card(key="format_card"):
    st.markdown("### 数据格式")
    st.markdown("CSV文件应包含以下字段")

    import pandas as pd
    format_df = pd.DataFrame({
        '字段': ['学号', '班级', '学习时长', '作业完成度', '考勤率', '测验成绩', '课堂参与度', '各科成绩'],
        '说明': ['学生编号', '所在班级', '每周学习时长（小时）', '作业完成百分比', '考勤百分比', '最近测验成绩', '1-5分', '编程/高数/英语/Python']
    })
    ui.table(format_df, key="format_table")

st.markdown("<br>", unsafe_allow_html=True)

# 技术栈
with ui.card(key="tech_card"):
    st.markdown("### 技术栈")
    st.markdown("")
    cols = st.columns(6)
    techs = ["Streamlit", "scikit-learn", "pandas", "matplotlib", "seaborn", "Python"]
    for i, tech in enumerate(techs):
        with cols[i]:
            st.markdown(f"""
            <div style="background: #f1f5f9; color: #475569; padding: 0.5rem 1rem; border-radius: 9999px; text-align: center; font-size: 0.875rem; font-weight: 500;">
                {tech}
            </div>
            """, unsafe_allow_html=True)

# 页脚
render_footer()
