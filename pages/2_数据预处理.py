"""
数据预处理页面
"""
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_section_header, render_info_card, render_metric_card, check_data_loaded
)
from data_processing import preprocess_data

# 页面配置
st.set_page_config(page_title="数据预处理", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题 - Apple 风格
st.markdown("""
<div class="page-header">
    <h1 class="page-title">数据预处理</h1>
    <p class="page-subtitle">处理缺失值、异常值并标准化数据</p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

# 初始化会话状态
if 'scaler' not in st.session_state:
    st.session_state['scaler'] = None

# 预处理区域 - Apple 风格布局
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    st.markdown("""
    <div class="custom-card">
        <h3>预处理选项</h3>
        <p>自动执行以下操作：</p>
        <ul style="color: #86868b; margin-top: 1rem; line-height: 2;">
            <li>缺失值填充（均值/众数）</li>
            <li>异常值处理（IQR方法）</li>
            <li>数据标准化（Z-score）</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    if st.button("执行预处理", type="primary", use_container_width=True):
        with st.spinner("处理中..."):
            df = st.session_state['df']
            df_processed, scaler = preprocess_data(df)
            st.session_state['df'] = df_processed
            st.session_state['scaler'] = scaler
        st.success("数据预处理完成！")
        st.rerun()

with col2:
    st.markdown("""
    <div class="custom-card">
        <h3>缺失值检查</h3>
        <p>检查各字段的缺失值情况</p>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state['df']
    missing_counts = df.isnull().sum()

    if missing_counts.sum() == 0:
        st.success("数据完整，无缺失值")
    else:
        missing_df = missing_counts[missing_counts > 0].reset_index()
        missing_df.columns = ['字段', '缺失数量']
        st.dataframe(missing_df, use_container_width=True)

# 显示预处理后的数据信息
if st.session_state['scaler'] is not None:
    st.markdown("---")

    st.markdown("""
    <div class="page-header">
        <h2 class="page-title">预处理结果</h2>
        <p class="page-subtitle">数据已标准化处理</p>
    </div>
    """, unsafe_allow_html=True)

    df = st.session_state['df']
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        render_metric_card("数据行数", len(df), " ")
    with col2:
        render_metric_card("数据列数", len(df.columns), " ")
    with col3:
        render_metric_card("缺失值总数", df.isnull().sum().sum(), "✓")

# 页脚
render_footer()
