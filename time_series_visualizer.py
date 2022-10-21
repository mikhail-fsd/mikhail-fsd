import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')
not_in_first_2_5 = df['value'] >= df['value'].quantile(0.025)
not_in_last_2_5 = df['value'] <= df['value'].quantile(0.975)

# Clean data
df = df[not_in_first_2_5 & not_in_last_2_5]


def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(15,5))
    ax.plot(df.index, df['value'], color='r')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig 


def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.resample('M').mean()
    df_bar['Month'] = df_bar.index.month_name()

    month_list = pd.date_range('2000', periods=12, freq='M').month_name()

    # Draw bar plot
    plt.figure(figsize=(8,8))
    g = sns.barplot(x=df_bar.index.year, y=df_bar.value, hue=df_bar['Month'], hue_order=month_list, edgecolor='white')
    plt.xticks(rotation='vertical')
    plt.xlabel('Years') 
    plt.ylabel('Average Page Views')
    plt.legend(loc='upper left', title='Month')
    plt.tight_layout()
    # Save image and return fig (don't change this part)
    fig = g.figure 
    fig.savefig('bar_plot.png')
    return fig


def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['Year'] = [d.year for d in df_box.date]
    df_box['Month'] = [d.strftime('%b') for d in df_box.date]
    df_box.rename(columns={'value': 'Page Views'}, inplace=True)

    # Draw box plots (using Seaborn)
    month_list = pd.date_range('2000', periods=12, freq='M').month_name().str[:3]
    
    fig, (ax1, ax2) = plt.subplots(1,2, figsize=(18,6))
    sns.boxplot(data=df_box, x='Year', y='Page Views', ax=ax1, fliersize=2)
    sns.boxplot(data=df_box, x='Month', y='Page Views', ax=ax2, order=month_list, fliersize=2)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax2.set_title('Month-wise Box Plot (Seasonality)')

    plt.tight_layout()

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_box_plot()
