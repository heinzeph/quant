import pandas as pd
import matplotlib.pyplot as plt
def human_readable_unit(x):
    """
    Gibt einen Faktor & Label zurück, um Werte schön darzustellen.
    """
    if x >= 1e12:
        return 1e12, 'Bio.'
    elif x >= 1e9:
        return 1e9, 'Mrd.'
    elif x >= 1e6:
        return 1e6, 'Mio.'
    elif x >= 1e3:
        return 1e3, 'Tsd.'
    else:
        return 1, ''
    
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
    row = row.squeeze()

    year_cols = [col for col in df.columns if isinstance(col, int)]
    years = sorted(year_cols)
    data = row[years]

    max_val = data.max()
    factor, unit = human_readable_unit(max_val)

    plt.figure(figsize=(10, 6))
    plt.plot(years, data.values / factor, marker='o')

    plt.title(f"{row['label']} [{row['concept']}]", fontsize=14)
    plt.xlabel("Jahr", fontsize=12)
    plt.ylabel(f"Wert ({unit})", fontsize=12)

    plt.xticks(years, rotation=45)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
    