"""
统计分析页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
from utils import load_custom_css, render_sidebar, render_footer
from data_processing import get_correlation_analysis, get_class_statistics, get_grade_distribution

# 页面配置
st.set_page_config(page_title="统计分析", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">统计分析</h1>
    <p style="font-size: 1.1rem; color: #64748b;">深入理解数据特征和相关性</p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
    with ui.card(key="empty_card"):
        st.markdown("###   请先加载数据")
        st.markdown("前往「数据加载」页面上传CSV文件或生成模拟数据")
    render_footer()
    st.stop()

df = st.session_state['df']

# 相关性分析
with ui.card(key="corr_card"):
    st.markdown("###   学习行为与成绩相关性")
    st.markdown("分析各学习行为指标与最终成绩的相关程度")
    corr_df = get_correlation_analysis(df)
    ui.table(corr_df.round(2), key="corr_table")

st.markdown("<br>", unsafe_allow_html=True)

# 班级统计
with ui.card(key="class_card"):
    st.markdown("###   班级学习状态统计")
    st.markdown("各班级的学习行为指标对比")
    class_stats = get_class_statistics(df)
    ui.table(class_stats, key="class_table")

st.markdown("<br>", unsafe_allow_html=True)

# 学业等级分布
with ui.card(key="grade_card"):
    st.markdown("###   学业等级分布")
    st.markdown("优、良、中、差各等级占比")
    grade_dist = get_grade_distribution(df)
    ui.table(grade_dist, key="grade_table")

# 页脚
render_footer()
