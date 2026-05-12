"""
模型评估页面
"""
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_metric_card, render_section_header, render_info_card,
    check_model_trained
)

# 页面配置
st.set_page_config(page_title="模型评估", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题 - Apple 风格
st.markdown("""
<div class="page-header">
    <h1 class="page-title">模型评估</h1>
    <p class="page-subtitle">查看模型的性能指标</p>
</div>
""", unsafe_allow_html=True)

# 检查模型是否已训练
if not check_model_trained():
    render_footer()
    st.stop()

metrics = st.session_state['metrics']

# 准确率展示 - Apple 风格
col1, col2 = st.columns(2, gap="large")
with col1:
    render_metric_card("训练集准确率", f"{metrics['train_accuracy']:.2%}", " ")
with col2:
    render_metric_card("测试集准确率", f"{metrics['test_accuracy']:.2%}", " ")

st.markdown("<br><br>", unsafe_allow_html=True)

# 分类报告
st.markdown("""
<div class="custom-card">
    <h3>分类报告</h3>
    <p>各类别的精确率、召回率、F1分数</p>
</div>
""", unsafe_allow_html=True)
st.text(metrics['class_report'])

st.markdown("<br><br>", unsafe_allow_html=True)

# 混淆矩阵
st.markdown("""
<div class="custom-card">
    <h3>混淆矩阵</h3>
    <p>预测结果与实际结果的对比</p>
</div>
""", unsafe_allow_html=True)
conf_matrix_df = pd.DataFrame(
    metrics['conf_matrix'],
    index=metrics['classes'],
    columns=metrics['classes']
)
st.dataframe(conf_matrix_df, use_container_width=True)

# 页脚
render_footer()
