
import streamlit as st
import joblib
import pandas as pd

# मोडेल लोड गर्नुहोस्
model = joblib.load('loan_model.pkl')

st.title("🏦 बैंक लोन जोखिम मूल्याङ्कन")
# यहाँ आफ्नो अघिको Streamlit को कोड राख्नुहोस्...
