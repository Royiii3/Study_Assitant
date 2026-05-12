"""
统计分析页面
"""
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_section_header, render_info_card, check_data_loaded
)
from data_processing import get_correlation_analysis, get_class_statistics, get_grade_distribution

# 页面配置
st.set_page_config(page_title="统计分析", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题 - Apple 风格
st.markdown("""
<div class="page-header">
    <h1 class="page-title">统计分析</h1>
    <p class="page-subtitle">深入理解数据特征和相关性</p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

df = st.session_state['df']

# 相关性分析
st.markdown("""
<div class="custom-card">
    <h3>学习行为与成绩相关性</h3>
    <p>分析各学习行为指标与最终成绩的相关程度</p>
</div>
""", unsafe_allow_html=True)
corr_df = get_correlation_analysis(df)
st.dataframe(corr_df.round(2), use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 班级统计
st.markdown("""
<div class="custom-card">
    <h3>班级学习状态统计</h3>
    <p>各班级的学习行为指标对比</p>
</div>
""", unsafe_allow_html=True)
class_stats = get_class_statistics(df)
st.dataframe(class_stats, use_container_width=True)

st.markdown("<br><br>", unsafe_allow_html=True)

# 学业等级分布
st.markdown("""
<div class="custom-card">
    <h3>学业等级分布</h3>
    <p>优、良、中、差各等级占比</p>
</div>
""", unsafe_allow_html=True)
grade_dist = get_grade_distribution(df)
st.dataframe(grade_dist, use_container_width=True)

# 页脚
render_footer()
