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
st.set_page_config(page_title="模型评估", page_icon=" ", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; margin: 0; font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        模型评估
    </h1>
    <p style="text-align: center; color: #6c757d; font-size: 1rem; margin-top: 0.5rem;">
        查看模型的性能指标
    </p>
</div>
""", unsafe_allow_html=True)

# 检查模型是否已训练
if not check_model_trained():
    render_footer()
    st.stop()

metrics = st.session_state['metrics']

# 准确率展示
col1, col2 = st.columns(2, gap="large")
with col1:
    render_metric_card("训练集准确率", f"{metrics['train_accuracy']:.2%}", " ")
with col2:
    render_metric_card("测试集准确率", f"{metrics['test_accuracy']:.2%}", " ")

st.markdown("<br>", unsafe_allow_html=True)

# 分类报告
render_info_card("分类报告", "各类别的精确率、召回率、F1分数")
st.text(metrics['class_report'])

st.markdown("<br>", unsafe_allow_html=True)

# 混淆矩阵
render_info_card("混淆矩阵", "预测结果与实际结果的对比")
conf_matrix_df = pd.DataFrame(
    metrics['conf_matrix'],
    index=metrics['classes'],
    columns=metrics['classes']
)
st.dataframe(conf_matrix_df, use_container_width=True)

# 页脚
render_footer()
