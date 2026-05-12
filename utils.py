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
    """加载自定义CSS样式 - Apple风格"""
    st.markdown("""
    <style>
    /* ===== Apple 风格全局样式 ===== */

    /* 导入系统字体 */
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

    /* 全局背景 - 纯白 */
    .stApp {
        background-color: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Noto Sans SC', 'SF Pro Display', 'Segoe UI', Roboto, sans-serif;
        color: #1d1d1f;
    }

    /* 主容器 - 大量留白 */
    .main .block-container {
        padding-top: 3rem;
        padding-bottom: 4rem;
        max-width: 1080px;
    }

    /* ===== 侧边栏 - 浅色极简 ===== */
    section[data-testid="stSidebar"] {
        background: #f5f5f7 !important;
        border-right: 1px solid #e8e8ed !important;
    }

    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown span {
        color: #1d1d1f !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #1d1d1f !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label p {
        color: #1d1d1f !important;
    }

    /* 侧边栏标题 */
    .sidebar-title {
        color: #1d1d1f !important;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        letter-spacing: -0.02em;
    }

    .sidebar-subtitle {
        color: #86868b !important;
        font-size: 0.85rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .sidebar-features {
        color: #86868b !important;
        font-size: 0.8rem;
        line-height: 2;
    }

    .sidebar-features span {
        display: block;
        padding: 0.25rem 0;
        color: #1d1d1f !important;
    }

    /* ===== 标题区域 - Apple Hero 风格 ===== */
    .hero-section {
        text-align: center;
        padding: 4rem 2rem 3rem;
        margin-bottom: 3rem;
    }

    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: -0.03em;
        line-height: 1.1;
        margin-bottom: 1rem;
        color: #1d1d1f;
    }

    .hero-subtitle {
        font-size: 1.25rem;
        font-weight: 400;
        color: #86868b;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.5;
    }

    /* ===== 卡片样式 - 极简白卡 ===== */
    .custom-card {
        background: #ffffff;
        border: 1px solid #e8e8ed;
        border-radius: 18px;
        padding: 2rem;
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .custom-card:hover {
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
        transform: translateY(-2px);
    }

    .custom-card h3 {
        font-size: 1.35rem;
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 0;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }

    .custom-card p {
        color: #86868b;
        font-size: 0.95rem;
        line-height: 1.6;
        margin: 0;
    }

    /* ===== 指标卡片 - Apple 风格 ===== */
    .metric-card {
        background: #f5f5f7;
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .metric-card:hover {
        background: #e8e8ed;
    }

    .metric-value {
        font-size: 3rem;
        font-weight: 700;
        color: #1d1d1f;
        margin: 0.5rem 0;
        letter-spacing: -0.03em;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #86868b;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* ===== 按钮样式 - Apple Blue ===== */
    .stButton > button {
        background: #0071e3 !important;
        color: white !important;
        border: none !important;
        border-radius: 980px !important;
        padding: 0.625rem 1.5rem !important;
        font-weight: 500 !important;
        font-size: 0.875rem !important;
        letter-spacing: -0.01em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: none !important;
        min-height: 40px !important;
        width: 100% !important;
    }

    .stButton > button:hover {
        background: #0077ed !important;
        transform: scale(1.02) !important;
        box-shadow: 0 2px 12px rgba(0, 113, 227, 0.3) !important;
    }

    .stButton > button:active {
        transform: scale(0.98) !important;
    }

    .stButton > button[type="primary"] {
        background: #0071e3 !important;
    }

    .stButton > button[kind="secondary"] {
        background: #f5f5f7 !important;
        color: #1d1d1f !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #e8e8ed !important;
    }

    /* ===== 分割线 - 细线 ===== */
    hr {
        border: none;
        height: 1px;
        background: #e8e8ed;
        margin: 2.5rem 0;
    }

    /* ===== 成功/警告框 ===== */
    .stSuccess {
        background: #f0f9f4 !important;
        border: 1px solid #bbf7d0 !important;
        border-radius: 12px !important;
        color: #166534 !important;
    }

    .stWarning {
        background: #fffbeb !important;
        border: 1px solid #fde68a !important;
        border-radius: 12px !important;
        color: #92400e !important;
    }

    .stError {
        background: #fef2f2 !important;
        border: 1px solid #fecaca !important;
        border-radius: 12px !important;
        color: #991b1b !important;
    }

    /* ===== 隐藏默认元素 ===== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== 页脚 ===== */
    .footer {
        text-align: center;
        color: #86868b;
        font-size: 0.85rem;
        margin-top: 5rem;
        padding-top: 2rem;
        border-top: 1px solid #e8e8ed;
    }

    .footer a {
        color: #0071e3;
        text-decoration: none;
    }

    /* ===== 动画 ===== */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ===== 功能卡片网格 ===== */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1.5rem;
        margin: 2rem 0;
    }

    .feature-item {
        background: #f5f5f7;
        border-radius: 18px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    .feature-item:hover {
        background: #e8e8ed;
        transform: translateY(-4px);
    }

    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .feature-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 0.5rem;
    }

    .feature-desc {
        font-size: 0.85rem;
        color: #86868b;
        line-height: 1.5;
    }

    /* ===== 页面标题 ===== */
    .page-header {
        margin-bottom: 3rem;
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1d1d1f;
        letter-spacing: -0.03em;
        margin-bottom: 0.75rem;
    }

    .page-subtitle {
        font-size: 1.1rem;
        color: #86868b;
        font-weight: 400;
    }

    /* ===== 预测结果卡片 ===== */
    .prediction-result {
        background: linear-gradient(135deg, #1d1d1f 0%, #2d2d30 100%);
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        color: white;
    }

    .prediction-grade {
        font-size: 5rem;
        font-weight: 700;
        letter-spacing: -0.05em;
        margin: 1rem 0;
    }

    .prediction-label {
        font-size: 1rem;
        color: #86868b;
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }

    /* ===== 步骤列表 ===== */
    .steps-list {
        list-style: none;
        padding: 0;
        counter-reset: step;
    }

    .steps-list li {
        counter-increment: step;
        padding: 1rem 0;
        border-bottom: 1px solid #e8e8ed;
        color: #1d1d1f;
        font-size: 1rem;
        line-height: 1.6;
    }

    .steps-list li:last-child {
        border-bottom: none;
    }

    .steps-list li::before {
        content: counter(step);
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        background: #0071e3;
        color: white;
        border-radius: 50%;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 1rem;
    }

    /* ===== 数据表格样式 ===== */
    .stDataFrame {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #e8e8ed !important;
    }

    /* ===== 选项卡样式 ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 1px solid #e8e8ed;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem !important;
        font-weight: 500 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #0071e3 !important;
        border-bottom: 2px solid #0071e3 !important;
    }

    /* ===== 滑块样式 ===== */
    .stSlider > div > div > div {
        background: #0071e3 !important;
    }

    /* ===== 响应式 ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }

        .page-title {
            font-size: 2rem;
        }

        .metric-value {
            font-size: 2rem;
        }

        .feature-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_metric_card(label, value, icon=""):
    """渲染指标卡片 - Apple 风格"""
    st.markdown(f"""
    <div class="metric-card fade-in">
        <div class="metric-label">{icon} {label}</div>
        <div class="metric-value">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def render_section_header(title, subtitle=""):
    """渲染章节标题 - Apple 风格"""
    st.markdown(f"""
    <div class="page-header">
        <h2 class="page-title">{title}</h2>
        {f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def render_info_card(title, description=""):
    """渲染信息卡片 - Apple 风格"""
    st.markdown(f"""
    <div class="custom-card">
        <h3>{title}</h3>
        {f'<p>{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)


def render_empty_state(icon, message, sub_message=""):
    """渲染空状态提示 - Apple 风格"""
    st.markdown(f"""
    <div class="custom-card" style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 3rem; margin-bottom: 1.5rem;">{icon}</div>
        <h3 style="color: #1d1d1f; font-size: 1.5rem; margin-bottom: 0.75rem;">{message}</h3>
        {f'<p style="color: #86868b; font-size: 1rem;">{sub_message}</p>' if sub_message else ''}
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """渲染侧边栏内容 - Apple 深色风格"""
    with st.sidebar:
        st.markdown('<div class="sidebar-title">学习行为分析</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-subtitle">
            基于机器学习的学业预测<br>与数据分析平台
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-features">
            <span>  数据驱动决策</span>
            <span>  机器学习预测</span>
            <span>  可视化分析</span>
        </div>
        """, unsafe_allow_html=True)


def render_footer():
    """渲染页脚 - Apple 风格"""
    st.markdown("""
    <div class="footer">
        <p>学习行为数据分析与学业预测系统</p>
        <p style="margin-top: 0.5rem;">Streamlit · scikit-learn · pandas · matplotlib</p>
    </div>
    """, unsafe_allow_html=True)


def render_feature_grid(features):
    """渲染功能网格 - Apple 风格"""
    html = '<div class="feature-grid">'
    for icon, title, desc in features:
        html += f"""
        <div class="feature-item">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)


def render_steps(steps):
    """渲染步骤列表 - Apple 风格"""
    html = '<ol class="steps-list">'
    for step in steps:
        html += f'<li>{step}</li>'
    html += '</ol>'
    st.markdown(html, unsafe_allow_html=True)


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
        render_empty_state(" ", "请先加载数据", "前往「数据加载」页面上传CSV文件或生成模拟数据")
        return False
    return True


def check_model_trained():
    """检查模型是否已训练，未训练则显示提示"""
    if 'model_trained' not in st.session_state or not st.session_state['model_trained']:
        render_empty_state(" ", "请先训练模型", "前往「学业预测」页面训练预测模型")
        return False
    return True
