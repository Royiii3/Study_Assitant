"""
工具函数模块
提供公共功能：字体配置、样式加载、数据验证等
"""

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from config import CHINESE_FONTS, BEHAVIOR_FEATURES


def setup_matplotlib_chinese():
    """配置matplotlib中文字体"""
    plt.rcParams['font.sans-serif'] = CHINESE_FONTS
    plt.rcParams['axes.unicode_minus'] = False


def load_custom_css():
    """加载自定义CSS样式"""
    st.markdown("""
    <style>
    /* 全局背景 */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* 主容器 */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1200px;
    }

    /* 侧边栏 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%) !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #ffffff !important;
    }

    /* 侧边栏标题 */
    .sidebar-title {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        padding-bottom: 0.8rem;
        border-bottom: 3px solid #3498db;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }

    /* 侧边栏装饰线 */
    .sidebar-decoration {
        background: linear-gradient(90deg, #3498db, #9b59b6);
        height: 5px;
        border-radius: 5px;
        margin: 1rem 0;
    }

    /* 卡片样式 */
    .custom-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1), 0 1px 3px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0,0,0,0.15), 0 3px 6px rgba(0,0,0,0.1);
    }

    /* 指标卡片 */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 1.2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 500;
    }

    /* 按钮样式 */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5) !important;
    }

    .stButton > button[type="primary"] {
        background: linear-gradient(135deg, #00b09b 0%, #96c93d 100%) !important;
        box-shadow: 0 4px 15px rgba(0, 176, 155, 0.4) !important;
    }

    /* 分割线 */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, #3498db, #9b59b6, #e74c3c);
        margin: 1.5rem 0;
    }

    /* 成功/警告框 */
    .stSuccess {
        border-left: 5px solid #2ecc71 !important;
    }

    .stWarning {
        border-left: 5px solid #f39c12 !important;
    }

    /* 隐藏默认元素 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 页脚 */
    .footer {
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #ecf0f1;
    }

    /* 动画 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, icon=""):
    """渲染指标卡片"""
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title, subtitle=""):
    """渲染章节标题"""
    st.markdown(f"""
    <div style="margin-bottom: 1.5rem;">
        <h2 style="margin-bottom: 0.5rem; color: #2c3e50;">{title}</h2>
        {f'<p style="color: #7f8c8d; font-size: 1.1rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title, description=""):
    """渲染信息卡片"""
    st.markdown(f"""
    <div class="custom-card">
        <h3 style="margin-top: 0;">{title}</h3>
        {f'<p style="color: #6c757d;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon, message, sub_message=""):
    """渲染空状态提示"""
    st.markdown(f"""
    <div class="custom-card" style="text-align: center; padding: 3rem;">
        <h3 style="color: #95a5a6;">{icon} {message}</h3>
        {f'<p style="color: #bdc3c7;">{sub_message}</p>' if sub_message else ''}
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """渲染侧边栏内容"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">  学习行为分析</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-decoration"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #ecf0f1; font-size: 0.9rem; margin: 0;">
                基于机器学习的学业预测与数据分析平台
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-decoration"></div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="text-align: center; padding: 1rem; color: #bdc3c7; font-size: 0.8rem;">
            <p>  数据驱动决策</p>
            <p>  机器学习预测</p>
            <p>  可视化分析</p>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """渲染页脚"""
    st.markdown("""
    <div class="footer">
        <p>© 2024 大学生学习行为数据分析与学业预测系统 | 基于机器学习技术</p>
        <p style="font-size: 0.8rem; color: #95a5a6;">使用 Streamlit + scikit-learn + pandas + matplotlib 构建</p>
    </div>
    """, unsafe_allow_html=True)


def validate_dataframe(df, required_columns=None):
    """验证DataFrame是否有效"""
    if df is None or df.empty:
        return False, "数据为空"
    if required_columns:
        missing = [col for col in required_columns if col not in df.columns]
        if missing:
            return False, f"缺少列: {', '.join(missing)}"
    return True, ""


def check_data_loaded():
    """检查数据是否已加载，未加载则显示提示"""
    if 'data_loaded' not in st.session_state or not st.session_state['data_loaded']:
        render_empty_state(" ", "请先加载数据", "在「数据加载」模块中上传CSV文件或生成模拟数据")
        return False
    return True


def check_model_trained():
    """检查模型是否已训练，未训练则显示提示"""
    if 'model_trained' not in st.session_state or not st.session_state['model_trained']:
        render_empty_state(" ", "请先训练模型", "在「学业预测」模块中训练预测模型")
        return False
    return True
