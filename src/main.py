import os
import sys
import logging
import fetcher
import fund
import pandas as pd
import visualizer
def main():
    pd.set_option('display.max_columns', None)  # Show all columns
    pd.set_option('display.max_rows', None)     # Show all rows
    balance_sheets, income_statements = fetcher.fetch_n_10ks_for_company("NVDA", 12)
    visualizer.visualize(balance_sheets, "Total Assets")
    print("s")
    
if __name__ == "__main__":
    main()
    