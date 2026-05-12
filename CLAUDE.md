# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **大学生学习行为数据分析与学业预测系统** (University Student Learning Behavior Analysis and Academic Prediction System) - a Streamlit web application for analyzing student learning data and predicting academic performance using machine learning.

## Tech Stack

- **Frontend/UI**: Streamlit (Python-based)
- **Data Analysis**: pandas, numpy
- **Visualization**: matplotlib, seaborn
- **Machine Learning**: scikit-learn (Logistic Regression)

## Project Structure

```
main.py              - Streamlit entry point and UI layout
data_processing.py   - Data loading, preprocessing, statistics
visualization.py     - Chart generation (6 plot functions)
prediction.py        - ML model training and prediction
requirements.txt     - Python dependencies
.streamlit/config.toml - Streamlit server configuration
```

## Running the Project

```bash
# Install dependencies
pip install -r requirements.txt

# Run Streamlit app
streamlit run main.py
```

## Architecture

**Module Dependencies**:
- `main.py` imports from all other modules
- `visualization.py` depends on `data_processing.py` for correlation data
- `prediction.py` handles model training and prediction independently

**Data Flow**:
1. User uploads CSV or generates synthetic data (200 samples)
2. `data_processing.py` handles missing values, outliers, normalization
3. `visualization.py` generates 6 chart types using matplotlib/seaborn
4. `prediction.py` trains LogisticRegression model (80/20 split)
5. Model predicts academic grade (优/良/中/差) from 5 input features

**Key Features in UI**:
- Data loading and preview
- Statistical analysis (correlation, class stats)
- 6 visualization types (bar, scatter, pie, line, heatmap, stacked bar)
- Grade prediction with probability distribution
- Model evaluation (accuracy, confusion matrix)

## Data Schema

The dataset uses Chinese column names:
- 学号, 班级, 性别 (ID, class, gender)
- 学习时长, 作业完成度, 考勤率, 测验成绩, 课堂参与度 (behavioral metrics)
- 编程成绩, 高数成绩, 英语成绩, Python成绩 (subject scores)
- 最终成绩, 学业等级 (final score, grade: 优/良/中/差)

## Notes for Development

- All UI text and data columns are in **Chinese**
- Charts use `SimHei` font for Chinese character support
- Streamlit session state manages app state across reruns
- Synthetic data generation uses `np.random.seed(42)` for reproducibility
- Model: LogisticRegression with lbfgs solver, max_iter=200
