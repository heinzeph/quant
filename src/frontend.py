import streamlit as st
import pandas as pd
from src.visualizer import visualize
from src.fetcher import fetch_n_10ks_for_company

st.title("📊 Finanzkennzahlen Dashboard")


ticker = st.text_input("Firmenticker eingeben (z.B. AAPL)", value="AAPL")
metric = st.selectbox("Welche Metrik möchtest du sehen?", [
    # Assets
    "Total Assets",
    "Current Assets",
    "Cash and Cash Equivalents",
    "Short-term Investments",
    "Accounts Receivable",
    "Inventory",
    "Prepaid Expenses",
    "Other Current Assets",
    "Property, Plant, and Equipment (Net)",
    "Goodwill",
    "Intangible Assets (Net)",
    "Other Non-current Assets",

    # Liabilities
    "Total Liabilities",
    "Current Liabilities",
    "Accounts Payable",
    "Accrued Expenses",
    "Deferred Revenue",
    "Short-term Debt",
    "Long-term Debt",
    "Pension & Postretirement Obligations",
    "Deferred Tax Liabilities",
    "Other Non-current Liabilities",

    # Equity
    "Total Stockholders’ Equity",
    "Common Stock",
    "Additional Paid-in Capital",
    "Retained Earnings / Accumulated Deficit",
    "Accumulated Other Comprehensive Income (Loss)",
    "Treasury Stock",

    # Sonstiges
    "Minority Interest / Non-controlling Interest",
    "Total Liabilities and Stockholders’ Equity"])
num_years = st.slider("Wieviele Jahre", min_value=1, max_value=10, value=5)

if st.button("Daten abrufen"):
    try:
        # Daten abrufen
        balance_sheets, income_statements = fetch_n_10ks_for_company(ticker, num_years)
        
        # Metrik über die Jahre plotten
        fig = visualize(balance_sheets, metric)
        st.success(f"Daten für {ticker} erfolgreich abgerufen!")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Daten: {e}")
