
import streamlit as st
import joblib
import pandas as pd


model = joblib.load('loan_model.pkl')

st.title("🏦 Bank loan risk score")

