from datetime import datetime
from datetime import date
from catdb.db.database import CatWeightDB
import pandas as pd
import matplotlib.pyplot as plt


def plot_weight_trends_by_years(df: pd.DataFrame, years: list[int], graph_file: str) -> None:
    """
    Plots weight changes over time for multiple years on the same graph.

    Parameters:
    - df (pd.DataFrame): The DataFrame containing 'date' and 'weight' columns.
    - years (list[int]): List of years to plot.

    Returns:
    - None
    """
    # Ensure 'date' column is in datetime format
    df['date'] = pd.to_datetime(df['date'])

    plt.figure(figsize=(12, 6))
    
    for year in years:
        # Filter data for the specific year
        df_year = df[df['date'].dt.year == year]
        
        if df_year.empty:
            print(f"No data available for the year {year}.")
            continue

        # Extract day of year for plotting purposes to align across years
        df_year = df_year.copy()  # Avoid SettingWithCopyWarning
        df_year['day_of_year'] = df_year['date'].dt.dayofyear

        # Plot the data for the year
        plt.plot(df_year['day_of_year'], df_year['weight'], marker='o', linestyle='-', label=str(year))

    # Labels and title
    plt.xlabel('Day of Year')
    plt.ylabel('Weight (kg)')
    plt.title('Cat Weight Trends by Year')
    plt.legend(title="Year")
    plt.grid()
    plt.tight_layout()

    plt.savefig(graph_file, format='png')
    print(f"Graph saved to {graph_file}")
    plt.close()


def graph_weight_records(db_file: str, graph_file: str | None = None) -> None:
    """
    Generates a graph of cat weight records over multiple years.
    Parameters:
    - db_file (str): Path to the database file.
    - graph_file (str | None): Output graph file name. If None, a default name will be used.    
    Returns:
    - None
    """
    db = CatWeightDB(db_file)
    db.connect()    
    df = db.get_all_records()

    # If no graph file is specified, use a default name.
    # Default name is 'cat_weight_YYYYMMDD_HHMM.png'.
    if graph_file is None:
        now = datetime.now()  # ← ここを修正
        graph_file = f"cat_weight_{now.strftime('%Y%m%d_%H%M')}.png"

    # years_sice_2021は2021年から今年までのリスト。今年を現在日時に基づいて更新
    current_year = date.today().year
    years_since_2021 = list(range(2021, current_year + 1))
    plot_weight_trends_by_years(df, years_since_2021, graph_file)

    db.close()
