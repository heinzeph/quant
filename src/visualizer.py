import pandas as pd
import matplotlib.pyplot as plt

def human_readable_unit(x):
    """
    Gibt einen Faktor & Label zurück, um Werte schön darzustellen.
    """
    print(x)
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

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(years, data.values / factor, marker='o')

    ax.set_title(f"{row['label']} [{row['concept']}]", fontsize=14)
    ax.set_xlabel("Jahr", fontsize=12)
    ax.set_ylabel(f"Wert ({unit})", fontsize=12)

    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.grid(True, linestyle='--', alpha=1)
    fig.tight_layout()

    return fig