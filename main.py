import streamlit as st
import pandas as pd
import numpy as np

# 导入自定义模块
from data_processing import (
    load_data, 
    preprocess_data, 
    get_correlation_analysis, 
    get_class_statistics,
    get_grade_distribution,
    generate_synthetic_data
)

from visualization import (
    plot_score_distribution,
    plot_behavior_score_correlation,
    plot_class_distribution,
    plot_learning_trend,
    plot_correlation_heatmap,
    plot_grade_by_class
)

from prediction import (
    train_prediction_model,
    predict_grade,
    prepare_training_data
)

def main():
    # 设置页面配置
    st.set_page_config(
        page_title="大学生学习行为数据分析与学业预测系统",
        page_icon="📊",
        layout="wide"
    )
    
    # 页面标题
    st.title("📊 大学生学习行为数据分析与学业预测系统")
    st.markdown("---")
    
    # 初始化会话状态
    if 'data_loaded' not in st.session_state:
        st.session_state['data_loaded'] = False
    if 'model_trained' not in st.session_state:
        st.session_state['model_trained'] = False
    if 'df' not in st.session_state:
        st.session_state['df'] = None
    if 'model' not in st.session_state:
        st.session_state['model'] = None
    if 'scaler' not in st.session_state:
        st.session_state['scaler'] = None
    if 'label_encoder' not in st.session_state:
        st.session_state['label_encoder'] = None
    if 'metrics' not in st.session_state:
        st.session_state['metrics'] = None
    
    # 侧边栏导航
    st.sidebar.title("导航菜单")
    menu_options = [
        "数据加载与预览",
        "数据预处理",
        "统计分析",
        "可视化展示",
        "学业预测",
        "模型评估"
    ]
    selected_menu = st.sidebar.radio("选择功能模块", menu_options)
    
    # 数据加载与预览模块
    if selected_menu == "数据加载与预览":
        st.subheader("📁 数据加载与预览")

        # 创建两列布局，分别放置上传和生成按钮
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**上传CSV文件**")
            uploaded_file = st.file_uploader("选择CSV文件", type=["csv"], label_visibility="collapsed")
            if st.button("上传并加载数据", type="primary", key="upload_btn"):
                if uploaded_file is not None:
                    try:
                        df = pd.read_csv(uploaded_file)
                        st.session_state['df'] = df
                        st.session_state['data_loaded'] = True
                        st.success("✅ CSV数据加载成功！")
                    except Exception as e:
                        st.error(f"❌ 数据加载失败: {e}")
                else:
                    st.warning("⚠️ 请先选择CSV文件")

        with col2:
            st.markdown("**使用模拟数据**")
            st.markdown("点击按钮自动生成200条模拟学习数据")
            if st.button("生成模拟数据", type="secondary", key="generate_btn"):
                df = generate_synthetic_data()
                st.session_state['df'] = df
                st.session_state['data_loaded'] = True
                st.success("✅ 模拟数据生成成功！")
        
        # 显示数据预览
        if st.session_state['data_loaded'] and st.session_state['df'] is not None:
            st.subheader("数据预览")
            # 让用户选择显示多少行数据
            num_rows = st.slider("选择显示的行数", min_value=5, max_value=len(st.session_state['df']), value=20, step=5)
            # 重置索引，让序号从1开始
            display_df = st.session_state['df'].head(num_rows).reset_index(drop=True)
            display_df.index = display_df.index + 1
            st.dataframe(display_df)
            st.caption(f"共 {len(st.session_state['df'])} 条数据，当前显示前 {num_rows} 条")
            
            # 数据基本信息
            st.subheader("数据基本信息")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("总学生数", len(st.session_state['df']))
            with col2:
                st.metric("班级数量", len(st.session_state['df']['班级'].unique()))
            with col3:
                st.metric("特征数量", len(st.session_state['df'].columns))
            
            # 数据统计摘要
            st.subheader("数据统计摘要")
            # 获取统计数据并添加中文说明
            stats_df = st.session_state['df'].describe()
            # 创建统计指标的中文说明
            stats_index_mapping = {
                'count': '样本数量',
                'mean': '平均值',
                'std': '标准差',
                'min': '最小值',
                '25%': '25%分位数',
                '50%': '中位数(50%分位数)',
                '75%': '75%分位数',
                'max': '最大值'
            }
            # 重命名索引
            stats_df = stats_df.rename(index=stats_index_mapping)
            # 显示带有说明
            with st.expander("查看统计指标说明"):
                st.markdown("""
                **统计指标说明：**
                - **样本数量 (count)**: 该字段的有效数据条数
                - **平均值 (mean)**: 该字段的平均水平
                - **标准差 (std)**: 数据离散程度的指标，数值越大波动越大
                - **最小值 (min)**: 该字段的最小值
                - **25%分位数**: 有25%的数据小于等于此值
                - **中位数 (50%分位数)**: 数据的中间值
                - **75%分位数**: 有75%的数据小于等于此值
                - **最大值 (max)**: 该字段的最大值
                """)
            st.dataframe(stats_df.round(2))
    
    # 数据预处理模块
    elif selected_menu == "数据预处理":
        st.subheader("🔧 数据预处理")
        
        if not st.session_state['data_loaded']:
            st.warning("请先在「数据加载与预览」模块加载数据")
            return
        
        if st.button("执行预处理"):
            with st.spinner("正在处理数据..."):
                df = st.session_state['df']
                df_processed, scaler = preprocess_data(df)
                st.session_state['df'] = df_processed
                st.session_state['scaler'] = scaler
                st.success("数据预处理完成！")
        
        # 显示预处理后的缺失值情况
        if st.session_state['df'] is not None:
            st.subheader("缺失值检查")
            missing_counts = st.session_state['df'].isnull().sum()
            st.dataframe(missing_counts[missing_counts > 0])
            
            if missing_counts.sum() == 0:
                st.success("✓ 没有缺失值")
    
    # 统计分析模块
    elif selected_menu == "统计分析":
        st.subheader("📈 统计分析")
        
        if not st.session_state['data_loaded']:
            st.warning("请先在「数据加载与预览」模块加载数据")
            return
        
        # 相关性分析
        st.subheader("学习行为与成绩相关性分析")
        corr_df = get_correlation_analysis(st.session_state['df'])
        st.dataframe(corr_df.round(2))
        
        # 班级统计
        st.subheader("班级学习状态统计")
        class_stats = get_class_statistics(st.session_state['df'])
        st.dataframe(class_stats)
        
        # 学业等级分布
        st.subheader("学业等级分布")
        grade_dist = get_grade_distribution(st.session_state['df'])
        st.dataframe(grade_dist)
    
    # 可视化展示模块
    elif selected_menu == "可视化展示":
        st.subheader("🎨 可视化展示")
        
        if not st.session_state['data_loaded']:
            st.warning("请先在「数据加载与预览」模块加载数据")
            return
        
        # 科目成绩分布柱状图
        st.subheader("科目成绩分布")
        fig1 = plot_score_distribution(st.session_state['df'])
        st.pyplot(fig1)
        
        # 学习行为与成绩关联散点图
        st.subheader("学习行为与成绩关联")
        fig2 = plot_behavior_score_correlation(st.session_state['df'])
        st.pyplot(fig2)
        
        # 班级学习状态分布饼图
        st.subheader("班级与学业等级分布")
        fig3 = plot_class_distribution(st.session_state['df'])
        st.pyplot(fig3)
        
        # 学期学习进度趋势折线图
        st.subheader("学期学习进度趋势")
        fig4 = plot_learning_trend(st.session_state['df'])
        st.pyplot(fig4)
        
        # 相关性热力图（额外功能）
        st.subheader("相关性热力图")
        corr_df = get_correlation_analysis(st.session_state['df'])
        fig5 = plot_correlation_heatmap(corr_df)
        st.pyplot(fig5)
        
        # 班级学业等级分布（额外功能）
        st.subheader("各班级学业等级分布")
        fig6 = plot_grade_by_class(st.session_state['df'])
        st.pyplot(fig6)
    
    # 学业预测模块
    elif selected_menu == "学业预测":
        st.subheader("🔮 学业等级预测")
        
        if not st.session_state['data_loaded']:
            st.warning("请先在「数据加载与预览」模块加载数据")
            return
        
        # 先训练模型
        if not st.session_state['model_trained']:
            if st.button("训练预测模型"):
                with st.spinner("正在训练模型..."):
                    df = st.session_state['df']
                    model, label_encoder, metrics = train_prediction_model(df)
                    st.session_state['model'] = model
                    st.session_state['label_encoder'] = label_encoder
                    st.session_state['metrics'] = metrics
                    st.session_state['model_trained'] = True
                    st.success("模型训练完成！")
            return
        
        # 用户输入表单
        st.subheader("输入您的学习行为数据")
        col1, col2 = st.columns(2)
        
        with col1:
            study_hours = st.slider("每周学习时长（小时）", min_value=1, max_value=40, value=15)
            homework_rate = st.slider("作业完成度（%）", min_value=0, max_value=100, value=85)
            attendance_rate = st.slider("考勤率（%）", min_value=0, max_value=100, value=90)
        
        with col2:
            quiz_score = st.slider("最近测验成绩（分）", min_value=0, max_value=100, value=75)
            participation = st.slider("课堂参与度（1-5）", min_value=1, max_value=5, value=3)
        
        # 预测按钮
        if st.button("预测学业等级"):
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
            
            # 显示预测结果
            st.subheader("预测结果")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("预测学业等级", prediction)
            
            with col2:
                st.write("各等级概率：")
                for grade, prob in prob_dict.items():
                    st.write(f"{grade}: {prob:.2%}")
    
    # 模型评估模块
    elif selected_menu == "模型评估":
        st.subheader("📊 模型评估")
        
        if not st.session_state['model_trained']:
            st.warning("请先在「学业预测」模块训练模型")
            return
        
        metrics = st.session_state['metrics']
        
        # 准确率展示
        st.subheader("模型准确率")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("训练集准确率", f"{metrics['train_accuracy']:.2%}")
        with col2:
            st.metric("测试集准确率", f"{metrics['test_accuracy']:.2%}")
        
        # 分类报告
        st.subheader("分类报告")
        st.text(metrics['class_report'])
        
        # 混淆矩阵
        st.subheader("混淆矩阵")
        conf_matrix_df = pd.DataFrame(
            metrics['conf_matrix'],
            index=metrics['classes'],
            columns=metrics['classes']
        )
        st.dataframe(conf_matrix_df)

if __name__ == "__main__":
    main()