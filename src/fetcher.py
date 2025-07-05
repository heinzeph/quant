from dotenv import load_dotenv
import os
import re
from email import policy
from email.parser import BytesParser
from bs4 import BeautifulSoup
import pandas as pd
import requests
from edgar import *
load_dotenv()
name = os.getenv("NAME")
email = os.getenv("EMAIL")
set_identity(email)

def combine_dfs(dfs: list[pd.DataFrame]) -> pd.DataFrame:
    """
    Combine a list of DataFrames into a single DataFrame.
    
    Args:
        dfs: List of DataFrames to combine.
        
    Returns:
        Combined DataFrame.
    """
    dfs_long = []

    for df in dfs:
        # identifiziere ID-Spalten
        id_vars = ["concept", "label", "level", "abstract", "dimension"]
        value_vars = [col for col in df.columns if col not in id_vars]

        df_long = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="date",
            value_name="value"
        )
        # parse Datum zu Jahr
        df_long["year"] = pd.to_datetime(df_long["date"]).dt.year
        df_long.drop(columns=["date"], inplace=True)
        dfs_long.append(df_long)

    combined = pd.concat(dfs_long, ignore_index=True)

    # jetzt pivotieren: Zeilen = concept+label…, Spalten = Jahre, Werte = value
    combined_wide = combined.pivot_table(
        index=["concept", "label", "level", "abstract", "dimension"],
        columns="year",
        values="value",
        aggfunc="first"
    ).reset_index()

    # Spalten sortieren (optional)
    combined_wide.columns.name = None
    year_cols = sorted([col for col in combined_wide.columns if isinstance(col, int)])
    ordered_cols = ["concept", "label", "level", "abstract", "dimension"] + year_cols
    combined_wide = combined_wide[ordered_cols]
    combined_wide = combined_wide.fillna(0)
    print(type(combined_wide))
    return combined_wide

def fetch_filings():
    

    c = Company("AAPL")
    filings = c.get_filings(form="10-K").latest(2)
    xbs = XBRL.from_filing(filings[1])
    income_statement = xbs.statements.income_statement()
    income_df = income_statement.to_dataframe()
    return income_df


def fetch_n_10ks_for_company(ticker: str, n: int):
    """
    Fetch the latest n filings for a company given its CIK.
    """
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
    balancesheets_final = combine_dfs(balancesheets)
    income_statements_final = combine_dfs(income_statements)
    return balancesheets_final, income_statements_final


