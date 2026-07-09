import streamlit as st
import pandas as pd

# -------------------------- 页面设置 --------------------------
st.set_page_config(page_title="APAP Individualized Dosage Assistant", layout="centered")
st.title("💊 Acetaminophen Individualized Dosage Assistant")
st.subheader("A Simple Tool to Help Calculate Safe and Effective Dosing")

# -------------------------- 输入模块 --------------------------
st.markdown("### 🧑‍⚕️ Patient Information Input")

col1, col2 = st.columns(2)
with col1:
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=25, step=1)
    weight = st.number_input("Weight (kg)", min_value=1.0, max_value=200.0, value=60.0, step=0.5)
with col2:
    indication = st.selectbox("Indication", ["Fever", "Mild Pain", "Moderate Pain"])
    liver_impairment = st.selectbox("Liver Function", ["Normal", "Impaired"])

# -------------------------- 计算模块 --------------------------
def calculate_dosage(age, weight, indication, liver_impairment):
    # 基础剂量：10-15 mg/kg/次，最大 1g/次，4g/天
    base_dose_mg_per_kg = 12
    if indication == "Fever":
        base_dose_mg_per_kg = 10
    elif indication == "Moderate Pain":
        base_dose_mg_per_kg = 15

    single_dose_mg = base_dose_mg_per_kg * weight
    max_single_dose_mg = 1000
    max_daily_dose_mg = 4000

    if liver_impairment == "Impaired":
        single_dose_mg *= 0.5
        max_daily_dose_mg = 2000

    single_dose_mg = round(min(single_dose_mg, max_single_dose_mg), 0)
    daily_dose_mg = round(min(single_dose_mg * 4, max_daily_dose_mg), 0)

    return {
        "Single Dose (mg)": single_dose_mg,
        "Max Daily Dose (mg)": daily_dose_mg,
        "Dosing Interval": "Every 4–6 hours, not exceeding 4 times daily"
    }

# -------------------------- 输出模块 --------------------------
if st.button("Calculate Recommended Dosage", use_container_width=True):
    result = calculate_dosage(age, weight, indication, liver_impairment)
    st.divider()
    st.markdown("## 📋 Recommended Dosage Summary")
    df_result = pd.DataFrame(list(result.items()), columns=["Parameter", "Recommendation"])
    st.dataframe(df_result, use_container_width=True, hide_index=True)

    st.markdown("### ⚠️ Important Safety Notes")
    st.info(
        "This tool is for educational purposes only. "
        "All dosing decisions must be confirmed by a healthcare professional. "
        "Do not exceed the maximum daily dose to avoid liver toxicity."
    )

st.divider()
st.caption(
    "Note: This system is a simplified auxiliary tool based on general dosing guidelines. "
    "It does not account for all individual factors. Always consult a physician or pharmacist."
)
