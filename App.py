%%writefile app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import builtins  # Standard Python round लाई ब्युँताउन

# Python Built-in round function
py_round = builtins.round

st.set_page_config(page_title="NRB - Loan Risk Engine", layout="wide")

st.title("🏦 NRB Real-Time Loan Risk Assessment Engine")

# Sidebar Simulator
st.sidebar.title("🧮 Live Loan Simulator")
applicant_income = st.sidebar.number_input("Applicant Income (NPR)", min_value=10000, value=75000, step=5000)
coapplicant_income = st.sidebar.number_input("Co-Applicant Income (NPR)", min_value=0, value=25000, step=5000)
loan_amount = st.sidebar.number_input("Loan Amount (NPR)", min_value=50000, value=1200000, step=50000)
credit_score = st.sidebar.slider("CIB Credit Score", min_value=300, max_value=850, value=680)
collateral_value = st.sidebar.number_input("Collateral Valuation (NPR)", min_value=100000, value=2500000, step=100000)

# Safe Feature Calculation (No PySpark Conflict)
total_income = applicant_income + coapplicant_income
dti_ratio = py_round(loan_amount / total_income, 2) if total_income > 0 else 0.0
ltv_ratio = py_round(loan_amount / collateral_value, 2) if collateral_value > 0 else 0.0

is_high_risk = (dti_ratio > 0.45) or (credit_score < 600) or (ltv_ratio > 0.80)
default_prob = 0.88 if is_high_risk else 0.08

# Display Metrics
col1, col2, col3 = st.columns(3)
col1.metric("DTI Ratio", f"{dti_ratio}", delta="Target < 0.45")
col2.metric("LTV Ratio", f"{ltv_ratio}", delta="Target < 0.80")
col3.metric("Credit Score", f"{credit_score}", delta="Target > 600")

if st.sidebar.button("Evaluate Risk", type="primary"):
    if is_high_risk:
        st.error(f"❌ STATUS: REJECTED (High Default Risk: {default_prob*100}%)")
    else:
        st.success(f"✅ STATUS: APPROVED (Low Risk: {default_prob*100}%)")
