"""
可视化展示页面
"""
import streamlit as st
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_section_header, check_data_loaded
)
from data_processing import get_correlation_analysis
from visualization import (
    plot_score_distribution,
    plot_behavior_score_correlation,
    plot_class_distribution,
    plot_learning_trend,
    plot_correlation_heatmap,
    plot_grade_by_class
)

# 页面配置
st.set_page_config(page_title="可视化展示 - 学习行为分析系统", page_icon=" ", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; margin: 0; font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
         可视化展示
    </h1>
    <p style="text-align: center; color: #6c757d; font-size: 1rem; margin-top: 0.5rem;">
        多维度图表分析
    </p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

df = st.session_state['df']

# 图表列表
charts = [
    ("  科目成绩分布", "各科目成绩的分数段分布情况", lambda: plot_score_distribution(df)),
    ("  学习行为与成绩关联", "学习行为指标与最终成绩的散点图分析", lambda: plot_behavior_score_correlation(df)),
    ("  班级与学业等级分布", "班级人数和学业等级的饼图分布", lambda: plot_class_distribution(df)),
    ("  学期学习进度趋势", "学期各周的学习指标变化趋势", lambda: plot_learning_trend(df)),
    ("  相关性热力图", "各指标之间的相关性热力图", lambda: plot_correlation_heatmap(get_correlation_analysis(df))),
    ("  各班级学业等级分布", "各班级学业等级的堆叠柱状图", lambda: plot_grade_by_class(df)),
]

# 渲染图表
for i, (title, desc, plot_func) in enumerate(charts):
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="margin-top: 0;">{title}</h3>
        <p style="color: #6c757d;">{desc}</p>
    </div>
    """, unsafe_allow_html=True)

    fig = plot_func()
    st.pyplot(fig)

    if i < len(charts) - 1:
        st.markdown("<br>", unsafe_allow_html=True)

# 页脚
render_footer()
