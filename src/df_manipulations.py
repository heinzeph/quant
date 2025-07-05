import pandas as pd

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
        # identify ID columns
        id_vars = ["concept", "label", "level", "abstract", "dimension"]
        value_vars = [col for col in df.columns if col not in id_vars]

        df_long = df.melt(
            id_vars=id_vars,
            value_vars=value_vars,
            var_name="date",
            value_name="value"
        )
        # parse date to year
        df_long["year"] = pd.to_datetime(df_long["date"]).dt.year
        df_long.drop(columns=["date"], inplace=True)
        dfs_long.append(df_long)

    combined = pd.concat(dfs_long, ignore_index=True)

    # now pivot: rows = concept+label…, columns = years, values = value
    combined_wide = combined.pivot_table(
        index=["concept", "label", "level", "abstract", "dimension"],
        columns="year",
        values="value",
        aggfunc="first"
    ).reset_index()

    # sort columns (optional)
    combined_wide.columns.name = None
    year_cols = sorted([col for col in combined_wide.columns if isinstance(col, int)])
    ordered_cols = ["concept", "label", "level", "abstract", "dimension"] + year_cols
    combined_wide = combined_wide[ordered_cols]
    combined_wide = combined_wide.fillna(0)
    print(type(combined_wide))
    return combined_wide

def extract_metrics_list(df):
    """
    Extracts a list of unique metrics from the DataFrame.
    
    Args:
        df: DataFrame containing financial data.
        
    Returns:
        List of unique metrics.
    """
    if 'concept' in df.columns:
        return df['label'].unique().tolist()
    else:
        raise ValueError("DataFrame does not contain 'concept' column.")
    
def drop_labels_without_numeric_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    Entfernt alle Zeilen, bei denen in den Datumsspalten (YYYY-MM-DD)
    kein numerischer Wert vorhanden ist.
    
    Args:
        df: DataFrame mit Spalten 'label', Datumsspalten, und weiteren Metadaten
    
    Returns:
        Bereinigter DataFrame
    """
    # nur Datumsspalten auswählen (die wie ein Datum aussehen)
    date_cols = [col for col in df.columns if _is_date(col)]
    
    # versuche alles in den Datumsspalten zu Zahlen zu konvertieren
    df_dates = df[date_cols].apply(pd.to_numeric, errors='coerce')
    
    # Maske: mind. eine Zahl in einer Datumsspalte
    has_numeric = df_dates.notna().any(axis=1)
    
    df_clean = df[has_numeric].reset_index(drop=True)
    return df_clean

def _is_date(s: str) -> bool:
    """Helper function: checks if column name looks like a date (YYYY-MM-DD)."""
    try:
        pd.to_datetime(s, format="%Y-%m-%d")
        return True
    except Exception:
        return False