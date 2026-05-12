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
    render_section_header, render_info_card, check_data_loaded
)
from data_processing import preprocess_data

# 页面配置
st.set_page_config(page_title="数据预处理", page_icon="⚙️", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); border-radius: 20px; padding: 2rem; margin-bottom: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.1);">
    <h1 style="text-align: center; margin: 0; font-size: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
        数据预处理
    </h1>
    <p style="text-align: center; color: #6c757d; font-size: 1rem; margin-top: 0.5rem;">
        处理缺失值、异常值并标准化数据
    </p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

# 初始化会话状态
if 'scaler' not in st.session_state:
    st.session_state['scaler'] = None

# 预处理区域
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    render_info_card("预处理选项", """
    自动执行以下操作：
    - 缺失值填充（均值/众数）
    - 异常值处理（IQR方法）
    - 数据标准化（Z-score）
    """)

    if st.button("执行预处理", type="primary", use_container_width=True):
        with st.spinner("处理中..."):
            df = st.session_state['df']
            df_processed, scaler = preprocess_data(df)
            st.session_state['df'] = df_processed
            st.session_state['scaler'] = scaler
        st.success("数据预处理完成！")
        st.rerun()

with col2:
    render_section_header("缺失值检查", "检查各字段的缺失值情况")

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
    render_section_header("预处理结果", "数据已标准化处理")

    df = st.session_state['df']
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("数据行数", len(df))
    with col2:
        st.metric("数据列数", len(df.columns))
    with col3:
        st.metric("缺失值总数", df.isnull().sum().sum())

# 页脚
render_footer()
