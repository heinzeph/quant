import pandas as pd
import matplotlib.pyplot as plt

def visualize (df, metric: str) -> None:
    """
    Visualize the data in a DataFrame.
    
    Args:
        data: DataFrame containing the data to visualize.
        
    Returns:
        None
    """
    

    row = df[(df['concept'] == metric) | (df['label'] == metric)]
    if row.empty:
        raise ValueError(f"Metric '{metric}' nicht gefunden!")

    row = row.squeeze()  # von DataFrame → Series

    # Jahr-Spalten herausfiltern
    year_cols = [col for col in df.columns if isinstance(col, int)]
    data = row[year_cols]

    plt.figure(figsize=(8,5))
    plt.plot(year_cols, data.values, marker='o')
    plt.title(f"{row['label']} ({row['concept']})")
    plt.xlabel("Jahr")
    plt.ylabel("Wert")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    