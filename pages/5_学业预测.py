"""
学业预测页面
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import streamlit as st
import streamlit_shadcn_ui as ui
import pandas as pd
from utils import load_custom_css, render_sidebar, render_footer
from prediction import train_prediction_model, predict_grade

# 页面配置
st.set_page_config(page_title="学业预测", layout="wide")
load_custom_css()
render_sidebar()

# 页面标题
st.markdown("""
<div style="margin-bottom: 2rem;">
    <h1 style="font-size: 2.5rem; font-weight: 700; color: #0f172a; letter-spacing: -0.03em;">学业等级预测</h1>
    <p style="font-size: 1.1rem; color: #64748b;">基于机器学习的学业等级预测</p>
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
if 'model_trained' not in st.session_state:
    st.session_state['model_trained'] = False
if 'model' not in st.session_state:
    st.session_state['model'] = None
if 'label_encoder' not in st.session_state:
    st.session_state['label_encoder'] = None
if 'metrics' not in st.session_state:
    st.session_state['metrics'] = None

# 训练模型
if not st.session_state['model_trained']:
    with ui.card(key="train_card"):
        st.markdown("###   训练预测模型")
        st.markdown("使用逻辑回归算法训练学业等级预测模型")
        st.markdown("")
        if ui.button("开始训练模型", key="train_btn", variant="default"):
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

# 用户输入表单
with ui.card(key="input_card"):
    st.markdown("###   输入学习行为数据")
    st.markdown("调整以下参数，预测学业等级")

col1, col2 = st.columns(2, gap="large")

with col1:
    study_hours = st.slider("每周学习时长（小时）", min_value=1, max_value=40, value=15)
    homework_rate = st.slider("作业完成度（%）", min_value=0, max_value=100, value=85)
    attendance_rate = st.slider("考勤率（%）", min_value=0, max_value=100, value=90)

with col2:
    quiz_score = st.slider("最近测验成绩（分）", min_value=0, max_value=100, value=75)
    participation = st.slider("课堂参与度（1-5）", min_value=1, max_value=5, value=3)

if ui.button("预测学业等级", key="predict_btn", variant="default"):
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

    # 预测结果
    with ui.card(key="result_card"):
        st.markdown(f"""
        <div style="text-align: center; padding: 2rem;">
            <p style="color: #64748b; text-transform: uppercase; letter-spacing: 0.1em; font-size: 0.875rem;">预测结果</p>
            <h1 style="font-size: 4rem; font-weight: 700; color: #0f172a; margin: 1rem 0;">{prediction}</h1>
            <p style="color: #64748b;">预测的学业等级</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 概率分布
    with ui.card(key="prob_card"):
        st.markdown("###   各等级概率分布")
        prob_df = pd.DataFrame({
            '学业等级': list(prob_dict.keys()),
            '概率': [f"{p:.2%}" for p in prob_dict.values()]
        })
        st.dataframe(prob_df, use_container_width=True)

# 页脚
render_footer()
