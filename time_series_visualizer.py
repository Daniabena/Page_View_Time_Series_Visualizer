import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")

df["date"] = pd.to_datetime(df["date"])
df= df.set_index("date")

# Clean data
low = df["value"].quantile(0.025)
high = df["value"].quantile(0.975)
df = df[(df["value"] >= low) & (df["value"] <= high)]
df = pd.DataFrame(df["value"])


def draw_line_plot():
    # Draw line plot
    fig, ax =plt.subplots(figsize=(15,5))

    ax.plot(df.index.values, df["value"].values, color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    ax.grid(False)

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar= df.copy()

    df_bar["year"] = df_bar.index.to_series().dt.year
    df_bar["month"] = df_bar.index.to_series().dt.month_name()

    table = df_bar.pivot_table(values="value", index="year", columns="month", aggfunc="mean")

    order=["January","February","March","April","May","June","July","August","September","October","November","December"]

    table = table.reindex(columns=order)

    # Draw bar plot
    ax =table.plot(kind="bar", figsize=(12,10))

    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")

    ax.legend(title="Months")
    fig = ax.get_figure()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()

    df_box= df_box.reset_index()

    df_box["year"]= df_box["date"].dt.year
    df_box["month"]= df_box["date"].dt.strftime("%b")

    month_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

    # Draw box plots (using Seaborn)
    fig, axes= plt.subplots(1,2, figsize=(20,6))

    sns.boxplot(data=df_box, x="year", y="value", ax=axes[0])

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(data=df_box, x="month",y="value",order=month_order, ax=axes[1])

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
