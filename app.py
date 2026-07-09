import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
plt.rcParams["font.sans-serif"] = ["WenQuanYi Zen Hei"]
plt.rcParams["axes.unicode_minus"] = False

# 你的实验原始数据集
dataset = [
    [25, 5, 0, 30, 0.1, 0, 2.40, 5.50, 1.100, 45.00, 0],
    [30, 0, 0, 30, 0.1, 0, 2.42, 4.57, 1.241, 40.82, 0],
    [25, 0, 8, 25, 0.1, 0.05, 2.40, 4.82, 1.1763, 37.70, 0],
    [25, 5, 0, 30, 0, 0, 0.233, 4.873, 1.1107, 8.89, 1],
    [25, 5, 0, 30, 0, 0, 2.65, 6.03, 1.134, 40.00, 0]
]

feature_names = ["丙二醇_mL", "甘油_mL", "PEG400_mL", "蔗糖_g", "桔子香精_g", "依地酸二钠_g"]
target_reg = ["主药含量(g/100mL)", "pH值", "相对密度", "黏度(mPa·s)"]
df = pd.DataFrame(dataset, columns=feature_names + target_reg + ["低温析出标签"])

X_raw = df[feature_names].values
y_content = df["主药含量(g/100mL)"].values
y_ph = df["pH值"].values
y_density = df["相对密度"].values
y_viscosity = df["黏度(mPa·s)"].values
y_precip = df["低温析出标签"].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)

# 训练AI预测模型
model_content = RandomForestRegressor(n_estimators=35, max_depth=4, random_state=2026)
model_ph = RandomForestRegressor(n_estimators=35, max_depth=4, random_state=2026)
model_density = RandomForestRegressor(n_estimators=35, max_depth=4, random_state=2026)
model_vis = RandomForestRegressor(n_estimators=35, max_depth=4, random_state=2026)
model_stability = RandomForestClassifier(n_estimators=35, max_depth=4, random_state=2026)

model_content.fit(X_scaled, y_content)
model_ph.fit(X_scaled, y_ph)
model_density.fit(X_scaled, y_density)
model_vis.fit(X_scaled, y_viscosity)
model_stability.fit(X_scaled, y_precip)

# 移动端适配网页界面
st.set_page_config(page_title="对乙酰氨基酚口服液AI预测模型", layout="centered")
st.title("💊 口服液处方AI预测系统")
st.subheader("基于实验处方数据预测含量、pH、黏度与低温稳定性")

st.markdown("### 输入每100mL处方辅料用量")
col1, col2 = st.columns(2)
with col1:
    propylene_glycol = st.number_input("丙二醇(mL)", min_value=0.0, max_value=50.0, value=25.0, step=0.5)
    glycerin = st.number_input("甘油(mL)", min_value=0.0, max_value=20.0, value=5.0, step=0.2)
    peg400 = st.number_input("PEG400(mL)", min_value=0.0, max_value=15.0, value=0.0, step=0.2)
with col2:
    sucrose = st.number_input("蔗糖(g)", min_value=0.0, max_value=50.0, value=30.0, step=1.0)
    orange_flavor = st.number_input("桔子香精(g)", min_value=0.0, max_value=0.5, value=0.1, step=0.01)
    edta_disodium = st.number_input("依地酸二钠(g)", min_value=0.0, max_value=0.1, value=0.0, step=0.01)

input_data = np.array([[propylene_glycol, glycerin, peg400, sucrose, orange_flavor, edta_disodium]])
input_processed = scaler.transform(input_data)

run_predict = st.button("一键运行AI预测", use_container_width=True)
if run_predict:
    pred_content = round(model_content.predict(input_processed)[0], 3)
    pred_ph = round(model_ph.predict(input_processed)[0], 2)
    pred_rd = round(model_density.predict(input_processed)[0], 4)
    pred_vis = round(model_vis.predict(input_processed)[0], 2)
    precip_prob = model_stability.predict_proba(input_processed)[0][1]
    stability_result = "微量析出，低温稳定性较差" if precip_prob > 0.5 else "无析出，低温稳定性合格"

    st.divider()
    st.markdown("## 📈 AI模型预测结果")
    result_table = pd.DataFrame({
        "检测项目": ["主药含量(g/100mL)", "pH", "相对密度", "黏度(mPa·s)", "低温储存表现"],
        "预测结果": [pred_content, pred_ph, pred_rd, pred_vis, stability_result]
    })
    st.dataframe(result_table, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("## 📊 辅料影响权重分析")
    feature_importance = model_content.feature_importances_
    fig, ax = plt.subplots(figsize=(8,3.5))
    ax.bar(feature_names, feature_importance)
    plt.xticks(rotation=35, fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)

st.caption("备注：模型由本次5组实验室处方数据训练生成，仅用作处方筛选参考，正式制剂仍需实验验证")
