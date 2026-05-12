"""
学业预测页面
"""
import sys
from pathlib import Path

# 添加项目根目录到 sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import pandas as pd
from utils import (
    load_custom_css, render_sidebar, render_footer,
    render_section_header, render_info_card, render_empty_state,
    check_data_loaded
)
from prediction import train_prediction_model, predict_grade

# 页面配置
st.set_page_config(page_title="学业预测", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题 - Apple 风格
st.markdown("""
<div class="page-header">
    <h1 class="page-title">学业等级预测</h1>
    <p class="page-subtitle">基于机器学习的学业等级预测</p>
</div>
""", unsafe_allow_html=True)

# 检查数据是否已加载
if not check_data_loaded():
    render_footer()
    st.stop()

# 初始化会话状态
if 'model_trained' not in st.session_state:
    st.session_state['model_trained'] = False
if 'model' not in st.session_state:
    st.session_state['model'] = None
if 'label_encoder' not in st.session_state:
    st.session_state['label_encoder'] = None
if 'metrics' not in st.session_state:
    st.session_state['metrics'] = None

# 训练模型 - Apple 风格
if not st.session_state['model_trained']:
    st.markdown("""
    <div class="custom-card" style="text-align: center; padding: 3rem;">
        <h3>训练预测模型</h3>
        <p>使用逻辑回归算法训练学业等级预测模型</p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("开始训练模型", type="primary", use_container_width=True):
        with st.spinner("模型训练中，请稍候..."):
            df = st.session_state['df']
            model, label_encoder, metrics = train_prediction_model(df)
            st.session_state['model'] = model
            st.session_state['label_encoder'] = label_encoder
            st.session_state['metrics'] = metrics
            st.session_state['model_trained'] = True
        st.success("模型训练完成！")
        st.rerun()

    render_footer()
    st.stop()

# 用户输入表单 - Apple 风格
st.markdown("""
<div class="custom-card">
    <h3>输入学习行为数据</h3>
    <p>调整以下参数，预测学业等级</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    study_hours = st.slider("每周学习时长（小时）", min_value=1, max_value=40, value=15)
    homework_rate = st.slider("作业完成度（%）", min_value=0, max_value=100, value=85)
    attendance_rate = st.slider("考勤率（%）", min_value=0, max_value=100, value=90)

with col2:
    quiz_score = st.slider("最近测验成绩（分）", min_value=0, max_value=100, value=75)
    participation = st.slider("课堂参与度（1-5）", min_value=1, max_value=5, value=3)

if st.button("预测学业等级", type="primary", use_container_width=True):
    input_data = {
        '学习时长': study_hours,
        '作业完成度': homework_rate,
        '考勤率': attendance_rate,
        '测验成绩': quiz_score,
        '课堂参与度': participation
    }

    prediction, prob_dict = predict_grade(
        st.session_state['model'],
        st.session_state['label_encoder'],
        st.session_state['scaler'],
        input_data
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 预测结果 - Apple 风格深色卡片
    st.markdown(f"""
    <div class="prediction-result">
        <div class="prediction-label">预测结果</div>
        <div class="prediction-grade">{prediction}</div>
        <div class="prediction-label">预测的学业等级</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    # 概率分布
    st.markdown("""
    <div class="custom-card">
        <h3>各等级概率分布</h3>
    </div>
    """, unsafe_allow_html=True)

    prob_df = pd.DataFrame({
        '学业等级': list(prob_dict.keys()),
        '概率': [f"{p:.2%}" for p in prob_dict.values()]
    })
    st.dataframe(prob_df, use_container_width=True)

# 页脚
render_footer()
