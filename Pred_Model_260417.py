import streamlit as st
import numpy as np

# ==================== Model Coefficients ====================
coef = {
    "Intercept": 8.14453174163429,
    "Age": -0.0329595346348611,
    "DM": -0.52811932797365,
    "Child": 1.19003691730742,
    "Tumor_Number": -0.927877698194275,
    "Max_Diameter": 0.0583263069525888,
    "PVTT": 0.117478592725974,
    "PIVKA_II": -5.89947870592201e-06,
    "ALB": -0.0089915355977858,
    "ALT": 0.00784097934484574,
    "AST": -0.00663548060755456,
    "TBIL": -0.0340714458533407,
    "AKP": -0.00153048695589896,
    "GGT": -0.00403577351913405,
    "PT": -0.239362341187477,
    "INR": -0.408776832006013,
    "Scr": -0.0118419322360738,
    "BUN": 0.0218423107648987,
    "WBC": 0.0926081487965438,
    "Hem": -0.00194972849606501,
    "BMI": -0.0193608324879867,
    "Neu_prop": -2.03783648487625,
}

# ==================== Page Configuration ====================
st.set_page_config(page_title="Clinical Prediction Calculator", page_icon="🧬", layout="wide")
st.title("🧬 Online Prediction Tool for Conversion to Surgery")
st.markdown("Please enter the patient's clinical parameters, and then click the button to obtain the predicted probability.")

# Sidebar for input controls
with st.sidebar:
    st.header("📋 Patient Information")
    age = st.number_input("Age (years)", min_value=0, max_value=120, value=55, step=1)
    dm = st.selectbox("Diabetes Mellitus (DM)", options=[0, 1], format_func=lambda x: "No" if x == 0 else "Yes")
    child = st.selectbox(
        "Child-Pugh Class",
        options=[1, 2],
        format_func=lambda x: "Class A" if x == 1 else "Class B"
    )
    tumor_num = st.number_input("Tumor Number", min_value=1, max_value=10, value=1, step=1)
    max_dia = st.number_input("Maximum Diameter (cm)", min_value=0.0, max_value=30.0, value=5.0, step=0.1)
    pvtt = st.selectbox("Portal Vein Tumor Thrombus (PVTT)", options=[0, 1],
                         format_func=lambda x: "No" if x == 0 else "Yes")
    pivka = st.number_input("PIVKA-II (mAU/mL)", min_value=0, value=100, step=10)
    alb = st.number_input("Albumin (ALB, g/L)", min_value=10.0, max_value=60.0, value=40.0, step=0.1)
    alt = st.number_input("Alanine Aminotransferase (ALT, U/L)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    ast = st.number_input("Aspartate Aminotransferase (AST, U/L)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    tbil = st.number_input("Total Bilirubin (TBIL, μmol/L)", min_value=0.0, max_value=500.0, value=15.0, step=0.1)
    akp = st.number_input("Alkaline Phosphatase (AKP, U/L)", min_value=0.0, max_value=500.0, value=80.0, step=1.0)
    ggt = st.number_input("Gamma-Glutamyl Transferase (GGT, U/L)", min_value=0.0, max_value=500.0, value=40.0, step=1.0)
    pt = st.number_input("Prothrombin Time (PT, seconds)", min_value=8.0, max_value=30.0, value=12.0, step=0.1)
    inr = st.number_input("International Normalized Ratio (INR)", min_value=0.8, max_value=5.0, value=1.0, step=0.01)
    scr = st.number_input("Serum Creatinine (Scr, μmol/L)", min_value=20.0, max_value=500.0, value=80.0, step=1.0)
    bun = st.number_input("Blood Urea Nitrogen (BUN, mmol/L)", min_value=1.0, max_value=30.0, value=5.0, step=0.1)
    wbc = st.number_input("White Blood Cell Count (WBC, 10⁹/L)", min_value=1.0, max_value=30.0, value=6.0, step=0.1)
    hem = st.number_input("Hemoglobin (Hem, g/L)", min_value=50.0, max_value=200.0, value=140.0, step=1.0)
    bmi = st.number_input("Body Mass Index (BMI, kg/m²)", min_value=15.0, max_value=50.0, value=22.0, step=0.1)
    neu_prop = st.number_input("Neutrophil Proportion (Neu_prop)", min_value=0.0, max_value=1.0, value=0.60, step=0.01)

    calc_button = st.button("🚀 Calculate Probability", type="primary", use_container_width=True)

# ==================== Main Panel: Display Results ====================
st.header("📊 Prediction Result")

if calc_button:
    # Calculate Linear Predictor (LP)
    lp = (coef["Intercept"] +
          coef["Age"] * age +
          coef["DM"] * dm +
          coef["Child"] * child +
          coef["Tumor_Number"] * tumor_num +
          coef["Max_Diameter"] * max_dia +
          coef["PVTT"] * pvtt +
          coef["PIVKA_II"] * pivka +
          coef["ALB"] * alb +
          coef["ALT"] * alt +
          coef["AST"] * ast +
          coef["TBIL"] * tbil +
          coef["AKP"] * akp +
          coef["GGT"] * ggt +
          coef["PT"] * pt +
          coef["INR"] * inr +
          coef["Scr"] * scr +
          coef["BUN"] * bun +
          coef["WBC"] * wbc +
          coef["Hem"] * hem +
          coef["BMI"] * bmi +
          coef["Neu_prop"] * neu_prop)
    
    # Calculate probability
    prob = 1 / (1 + np.exp(-lp))
    
    # Display metrics
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Linear Predictor (LP)", f"{lp:.4f}")
    with col2:
        st.metric("Predicted Probability", f"{prob * 100:.2f}%")
    
    # Visual risk bar
    st.progress(float(prob), text=f"Probability: {prob*100:.1f}%")
    
    st.markdown("---")
    st.caption("Formula: P = 1 / (1 + exp(-LP))")
else:
    st.info("👈 Please fill in the patient information on the left and click the 'Calculate Probability' button.")

# ==================== Footer ====================
st.markdown("---")
st.markdown("**Disclaimer**: This tool is for research and academic communication purposes only and cannot replace professional clinical diagnosis.")
