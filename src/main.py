import os
import sys
import logging
import fetcher
import fund
import pandas as pd
import visualizer
import df_manipulations
def main():
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)     # Show all rows
    balance_sheets, income_statements = fetcher.fetch_n_10ks_for_company("AAPL", 1)
    visualizer.visualize(balance_sheets, "Total Assets")
    balance_sheets = df_manipulations.drop_labels_without_numeric_values(balance_sheets)
    print(balance_sheets)
    
if __name__ == "__main__":
    main()
    