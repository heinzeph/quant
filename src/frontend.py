import streamlit as st
import pandas as pd
from visualizer import visualize
from fetcher import fetch_n_10ks_for_company

st.title("📊 Finanzkennzahlen Dashboard")


ticker = st.text_input("Firmenticker eingeben (z.B. AAPL oder MCSF)", value="AAPL")
num_years = st.slider("Wieviele Jahre", min_value=1, max_value=10, value=5)

if st.button("Daten abrufen"):
    try:
        # Daten abrufen
        balance_sheets, income_statements, balance_sheets_metrics, income_statements_metrics= fetch_n_10ks_for_company(ticker, num_years)
        st.session_state['balance_sheets'] = balance_sheets
        st.session_state['income_statements'] = income_statements
        st.session_state['balance_sheets_metrics'] = balance_sheets_metrics
        st.session_state['income_statements_metrics'] = income_statements_metrics
        st.session_state['ready'] = True
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
   
if st.session_state.get('ready'):
    category = st.selectbox("Welche Kategorie?", ["Bilanz", "GuV"])

    if category == "Bilanz":
        metric = st.selectbox("Welche Kennzahl?", st.session_state['balance_sheets_metrics'])
        relevant_df = st.session_state['balance_sheets']
    else:
        metric = st.selectbox("Welche Kennzahl?", st.session_state['income_statements_metrics'])
        relevant_df = st.session_state['income_statements']

    if st.button("📊 Visualisieren"):
        fig = visualize(relevant_df, metric)
        st.pyplot(fig)
