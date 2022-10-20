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

#group_names = ['sdf', 'sdfsd', 'sdfsdf']
#group_data = [1,2,3]
#fig, ax = plt.subplots(figsize=(8, 8))
#ax.barh(group_names, group_data)

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
    print(type(df_bar))
    print(df.info())
    print(df_bar.head())
    # Draw bar plot

    dada ={'first': ['a', 'b', 'c'], 'second': [1,2,3]}
    df_dada = pd.DataFrame(dada)
    sns.catplot(data=df_dada, x='first', y='second', kind='bar')  # it works
    df_bar.reset_index(inplace=True)
    print(df_bar.head())
    sns.catplot(data=df_bar, x='date', y='value', kind='bar') 

    #plt.bar(df_bar.index, df_bar['value'], width=8)
    #sns.catplot(df_bar, kind='bar')

    #sns.barplot(df_bar, x=df_bar.index, y=df_bar['value']) 
    plt.gcf().autofmt_xdate()
    plt.show()
        


    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)





    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig

draw_bar_plot()
