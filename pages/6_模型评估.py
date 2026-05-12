"""
模型评估页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from utils import load_custom_css, render_sidebar, render_footer, render_metric_card

# 页面配置
st.set_page_config(page_title="模型评估", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">模型评估</h1>
    <p style="font-size: 1.1rem; color: #64748b;">查看模型的性能指标</p>
</div>
""", unsafe_allow_html=True)

# 检查模型是否已训练
if 'model_trained' not in st.session_state or not st.session_state['model_trained']:
    with ui.card(key="empty_card"):
        st.markdown("###   请先训练模型")
        st.markdown("前往「学业预测」页面训练预测模型")
    render_footer()
    st.stop()

metrics = st.session_state['metrics']

# 准确率展示
col1, col2 = st.columns(2, gap="large")
with col1:
    render_metric_card("训练集准确率", f"{metrics['train_accuracy']:.2%}", " ")
with col2:
    render_metric_card("测试集准确率", f"{metrics['test_accuracy']:.2%}", " ")

st.markdown("<br><br>", unsafe_allow_html=True)

# 分类报告
with ui.card(key="report_card"):
    st.markdown("###   分类报告")
    st.markdown("各类别的精确率、召回率、F1分数")
    st.text(metrics['class_report'])

st.markdown("<br>", unsafe_allow_html=True)

# 混淆矩阵
with ui.card(key="matrix_card"):
    st.markdown("###   混淆矩阵")
    st.markdown("预测结果与实际结果的对比")
    conf_matrix_df = pd.DataFrame(
        metrics['conf_matrix'],
        index=metrics['classes'],
        columns=metrics['classes']
    )
    st.dataframe(conf_matrix_df, use_container_width=True)

# 页脚
render_footer()
