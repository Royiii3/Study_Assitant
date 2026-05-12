"""
可视化展示页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
from utils import load_custom_css, render_sidebar, render_footer
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
st.set_page_config(page_title="可视化展示", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">可视化展示</h1>
    <p style="font-size: 1.1rem; color: #64748b;">多维度图表分析</p>
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

# 图表列表
charts = [
    ("科目成绩分布", "各科目成绩的分数段分布情况", lambda: plot_score_distribution(df)),
    ("学习行为与成绩关联", "学习行为指标与最终成绩的散点图分析", lambda: plot_behavior_score_correlation(df)),
    ("班级与学业等级分布", "班级人数和学业等级的饼图分布", lambda: plot_class_distribution(df)),
    ("学期学习进度趋势", "学期各周的学习指标变化趋势", lambda: plot_learning_trend(df)),
    ("相关性热力图", "各指标之间的相关性热力图", lambda: plot_correlation_heatmap(get_correlation_analysis(df))),
    ("各班级学业等级分布", "各班级学业等级的堆叠柱状图", lambda: plot_grade_by_class(df)),
]

# 渲染图表
for i, (title, desc, plot_func) in enumerate(charts):
    with ui.card(key=f"chart_{i}"):
        st.markdown(f"### {title}")
        st.markdown(desc)
        fig = plot_func()
        st.plotly_chart(fig, use_container_width=True)

    if i < len(charts) - 1:
        st.markdown("<br>", unsafe_allow_html=True)

# 页脚
render_footer()
