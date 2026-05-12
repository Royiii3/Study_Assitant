"""
数据加载与预览页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from utils import load_custom_css, render_sidebar, render_footer, render_metric_card
from data_processing import generate_synthetic_data

# 页面配置
st.set_page_config(page_title="数据加载", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">数据加载</h1>
    <p style="font-size: 1.1rem; color: #64748b;">上传数据文件或使用模拟数据开始分析</p>
</div>
""", unsafe_allow_html=True)

# 初始化会话状态
if 'data_loaded' not in st.session_state:
    st.session_state['data_loaded'] = False
if 'df' not in st.session_state:
    st.session_state['df'] = None

# 数据加载区域
col1, col2 = st.columns(2, gap="large")

with col1:
    with ui.card(key="upload_card"):
        st.markdown("###   上传数据文件")
        st.markdown("支持CSV格式的数据文件")
        st.markdown("")
        uploaded_file = st.file_uploader("选择CSV文件", type=["csv"], label_visibility="collapsed")
        if ui.button("上传并加载数据", key="upload_btn", variant="default"):
            if uploaded_file is not None:
                try:
                    df = pd.read_csv(uploaded_file)
                    st.session_state['df'] = df
                    st.session_state['data_loaded'] = True
                    st.success("数据加载成功！")
                    st.rerun()
                except Exception as e:
                    st.error(f"数据加载失败: {e}")
            else:
                st.warning("请先选择CSV文件")

with col2:
    with ui.card(key="synthetic_card"):
        st.markdown("###   使用模拟数据")
        st.markdown("自动生成200条模拟学习数据")
        st.markdown("")
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
            <p style="color: #64748b; font-size: 0.875rem; margin: 0;">
                包含学习时长、作业完成度、考勤率、测验成绩、课堂参与度等字段
            </p>
        </div>
        """, unsafe_allow_html=True)
        if ui.button("生成模拟数据", key="generate_btn", variant="secondary"):
            df = generate_synthetic_data()
            st.session_state['df'] = df
            st.session_state['data_loaded'] = True
            st.success("模拟数据生成成功！")
            st.rerun()

# 显示数据预览
if st.session_state['data_loaded'] and st.session_state['df'] is not None:
    df = st.session_state['df']

    st.markdown("---")

    # 指标卡片
    col1, col2, col3 = st.columns(3, gap="medium")
    with col1:
        render_metric_card("总学生数", len(df), " ")
    with col2:
        render_metric_card("班级数量", len(df['班级'].unique()), " ")
    with col3:
        render_metric_card("特征数量", len(df.columns), " ")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 数据预览
    st.markdown("### 数据预览")
    st.markdown("*查看数据集的详细信息*")
    num_rows = st.slider("显示行数", min_value=5, max_value=len(df), value=20, step=5)
    display_df = df.head(num_rows).reset_index(drop=True)
    display_df.index = display_df.index + 1
    st.dataframe(display_df, use_container_width=True)
    st.caption(f"共 {len(df)} 条数据，当前显示前 {num_rows} 条")

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 数据统计摘要
    st.markdown("### 数据统计摘要")
    st.markdown("*各字段的统计指标*")
    stats_df = df.describe()
    stats_index_mapping = {
        'count': '样本数量', 'mean': '平均值', 'std': '标准差',
        'min': '最小值', '25%': '25%分位数', '50%': '中位数',
        '75%': '75%分位数', 'max': '最大值'
    }
    stats_df = stats_df.rename(index=stats_index_mapping)
    st.dataframe(stats_df.round(2), use_container_width=True)

    with st.expander("查看统计指标说明"):
        st.markdown("""
        - **样本数量 (count)**: 该字段的有效数据条数
        - **平均值 (mean)**: 该字段的平均水平
        - **标准差 (std)**: 数据离散程度，数值越大波动越大
        - **最小值 (min)**: 该字段的最小值
        - **25%分位数**: 有25%的数据小于等于此值
        - **中位数 (50%分位数)**: 数据的中间值
        - **75%分位数**: 有75%的数据小于等于此值
        - **最大值 (max)**: 该字段的最大值
        """)

# 页脚
render_footer()
