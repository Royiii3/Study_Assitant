"""
数据预处理页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
from utils import load_custom_css, render_sidebar, render_footer, render_metric_card
from data_processing import preprocess_data

# 页面配置
st.set_page_config(page_title="数据预处理", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">数据预处理</h1>
    <p style="font-size: 1.1rem; color: #64748b;">处理缺失值、异常值并标准化数据</p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
    with ui.card(key="empty_card"):
        st.markdown("###   请先加载数据")
        st.markdown("前往「数据加载」页面上传CSV文件或生成模拟数据")
    render_footer()
    st.stop()

# 初始化会话状态
if 'scaler' not in st.session_state:
    st.session_state['scaler'] = None

# 预处理区域
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    with ui.card(key="options_card"):
        st.markdown("### ⚙️ 预处理选项")
        st.markdown("自动执行以下操作：")
        st.markdown("""
        - 缺失值填充（均值/众数）
        - 异常值处理（IQR方法）
        - 数据标准化（Z-score）
        """)
        st.markdown("")
        if ui.button("执行预处理", key="preprocess_btn", variant="default"):
            with st.spinner("处理中..."):
                df = st.session_state['df']
                df_processed, scaler = preprocess_data(df)
                st.session_state['df'] = df_processed
                st.session_state['scaler'] = scaler
            st.success("数据预处理完成！")
            st.rerun()

with col2:
    with ui.card(key="missing_card"):
        st.markdown("###   缺失值检查")
        st.markdown("检查各字段的缺失值情况")

        df = st.session_state['df']
        missing_counts = df.isnull().sum()

        if missing_counts.sum() == 0:
            st.success("数据完整，无缺失值")
        else:
            missing_df = missing_counts[missing_counts > 0].reset_index()
            missing_df.columns = ['字段', '缺失数量']
            ui.table(missing_df, key="missing_table")

# 显示预处理后的数据信息
if st.session_state['scaler'] is not None:
    st.markdown("---")

    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 style="font-size: 2rem; font-weight: 700; color: #0f172a;">预处理结果</h2>
        <p style="color: #64748b;">数据已标准化处理</p>
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
