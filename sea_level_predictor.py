import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress


def draw_plot():
    # Read data from file
    df = pd.read_csv('epa-sea-level.csv')

    # Create scatter plot
    plt.scatter(x=df['Year'], y=df['CSIRO Adjusted Sea Level'])
    
    # Create first line of best fit
    res1 = linregress(df['Year'], df['CSIRO Adjusted Sea Level'])
    years = np.arange(1880, 2051)
    plt.plot(years, res1.intercept + res1.slope*years, 'g')

    # Create second line of best fit
    df2 = df.set_index('Year') 
    res2 = linregress(df2.loc[2000:].index, df2.loc[2000:]['CSIRO Adjusted Sea Level'])
    years = np.arange(2000, 2051)
    plt.plot(years, res2.intercept + res2.slope*years, 'r')

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('Sea Level (inches)')
    plt.title('Rise in Sea Level')
    
    # Save plot and return data for testing (DO NOT MODIFY)
    plt.savefig('sea_level_plot.png')
    return plt.gca()

draw_plot()



