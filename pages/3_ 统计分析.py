"""
统计分析页面
"""
import streamlit as st
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_section_header, render_info_card, check_data_loaded
)
from data_processing import get_correlation_analysis, get_class_statistics, get_grade_distribution

# 页面配置
st.set_page_config(page_title="统计分析 - 学习行为分析系统", page_icon=" ", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; margin: 0; font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
         统计分析
    </h1>
    <p style="text-align: center; color: #6c757d; font-size: 1rem; margin-top: 0.5rem;">
        深入理解数据特征和相关性
    </p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

df = st.session_state['df']

# 相关性分析
render_info_card("  学习行为与成绩相关性", "分析各学习行为指标与最终成绩的相关程度")
corr_df = get_correlation_analysis(df)
st.dataframe(corr_df.round(2), use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 班级统计
render_info_card("  班级学习状态统计", "各班级的学习行为指标对比")
class_stats = get_class_statistics(df)
st.dataframe(class_stats, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# 学业等级分布
render_info_card("  学业等级分布", "优、良、中、差各等级占比")
grade_dist = get_grade_distribution(df)
st.dataframe(grade_dist, use_container_width=True)

# 页脚
render_footer()
