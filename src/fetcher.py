from dotenv import load_dotenv
import os
import re
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from edgar import *
import df_manipulations
load_dotenv()
name = os.getenv("NAME")
email = os.getenv("EMAIL")
set_identity(email)



def fetch_filings():

    c = Company("AAPL")
    filings = c.get_filings(form="10-K").latest(2)
    xbs = XBRL.from_filing(filings[1])
    income_statement = xbs.statements.income_statement()
    income_df = income_statement.to_dataframe()
    return income_df

def fetch_latest_10k(ticker: str):
    c = Company(ticker)
    filing = c.get_filings(form="10-K").latest()
    xb =filing.xbrl()
    statements = xb.statements
    # Display financial statements
    balance_sheet = statements.balance_sheet()
    income_statement = statements.income_statement()
    return (
        balance_sheet.to_dataframe(),
        income_statement.to_dataframe()
    )
def fetch_n_10ks_for_company(ticker: str, n: int):
    """
    Fetches and processes the latest n 10-K filings for a given company ticker.

    Args:
        ticker (str): The stock ticker symbol of the company (e.g., "AAPL").
        n (int): The number of most recent 10-K filings to retrieve.

    Returns:
        tuple: Contains four elements:
            - balancesheets_final (pd.DataFrame): Combined DataFrame of balance sheets from the filings.
            - income_statements_final (pd.DataFrame): Combined DataFrame of income statements from the filings.
            - balancesheets_metric_list (list): List of unique metrics found in the balance sheets.
            - income_statements_metric_list (list): List of unique metrics found in the income statements.
    """
    if n == 1:
        return fetch_latest_10k(ticker)
    c = Company(ticker)
    filings = c.get_filings(form="10-K").latest(n)
    income_statements = []
    balancesheets = []
    for filing in filings:
        xbrl = XBRL.from_filing(filing)
        income_statement = xbrl.statements.income_statement()
        balance_sheet = xbrl.statements.balance_sheet()
        income_statements.append(income_statement.to_dataframe())
        balancesheets.append(balance_sheet.to_dataframe())
    balancesheets_final = df_manipulations.combine_dfs(balancesheets)
    income_statements_final = df_manipulations.combine_dfs(income_statements)
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)     # Show all rows
    print(balancesheets_final)
    return balancesheets_final, income_statements_final