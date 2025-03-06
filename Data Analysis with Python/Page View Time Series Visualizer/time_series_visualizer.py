import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
import matplotlib.dates as mdates

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv")

# Clean data
df = df[(df['value'] >= df['value'].quantile(0.025)) & (df['value'] <= df['value'].quantile(0.975))]

month_order = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
    'Sep', 'Oct', 'Nov', 'Dec'
]

month_order_full = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
    'September', 'October', 'November', 'December'
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    line_plot = plt.plot(df["date"], df["value"])

    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))  # Every 6 months
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y'))

    plt.xlabel("Date")
    plt.ylabel("Page Views")
    plt.title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    pass
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['date'] = pd.to_datetime(df_bar['date'])
    df_bar['Year'] = [d.year for d in df_bar.date]
    df_bar['Month'] = [d.strftime('%b') for d in df_bar.date]
    
    df_bar = df_bar.groupby(['Year', 'Month'])['value'].mean().reset_index()
    df_bar['Month'] = pd.Categorical(df_bar['Month'], categories=month_order, ordered=True)
    # print(df_bar[:3])
    # Draw bar plot 
    fig, ax = plt.subplots(figsize=(10,10))
    bar_plot = sns.barplot(data=df_bar, x='Year', y='value', hue='Month', palette = 'dark')
    # fig = bar_plot.fig
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
   # Modify Legend Labels to Full Month Names
    handles, labels = ax.get_legend_handles_labels()
    month_mapping = dict(zip(month_order, month_order_full))
    new_labels = [month_mapping[label] for label in labels]
    ax.legend(handles, new_labels, title="Months")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['date'] = pd.to_datetime(df_box['date'])
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))
    sns.boxplot(df_box, x = 'year', y='value', ax=ax[0], hue='year', legend=False)
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    sns.boxplot(df_box, x = 'month', y='value', ax=ax[1],hue='month', order=month_order)
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
