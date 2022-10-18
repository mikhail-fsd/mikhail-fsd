import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np



# Import data
df = pd.read_csv('medical_examination.csv')
# Add 'overweight' column
df['overweight'] = [0 if x < 25 else 1 for x in (df['weight'] / (df['height']/100)**2) ]
# Normalize data by making 0 always good and 1 always bad. If the value of 'cholesterol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.
df['cholesterol'] = [0 if x == 1 else 1 for x in df['cholesterol']]
df['gluc'] = [0 if x == 1 else 1 for x in df['gluc']]

# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_melt_cardio = df.melt(id_vars=['cardio'], value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cardio_group = df_melt_cardio.groupby(['cardio', 'variable'])
    df_cardio_group.value_counts()
    
    # Draw the catplot with 'sns.catplot()'
    ax = sns.catplot(data=df_melt_cardio, x='variable', hue='value', col='cardio', kind='count').set(ylabel='total')
    
    # Get the figure for the output
    fig = ax.figure 

    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():

    # incorrect data filters
    # diastolic pressure is higher than systolic 
    filter1 = df['ap_lo'] <= df['ap_hi']
    # height is less than the 2.5th percentile
    filter2 = df['height'] >= df['height'].quantile(0.025)
    # height is more than the 97.5th percentile
    filter3 = df['height'] <= np.percentile(df['height'], 97.5) 
    # weight is less than the 2.5th percentile
    filter4 = df['weight'] >= np.percentile(df['weight'], 2.5) 
    # weight is more than the 97.5th percentile
    filter5 = df['weight'] <= np.percentile(df['weight'], 97.5) 

    # Clean the data
    df_heat = df[(filter1) & (filter2) & (filter3) & (filter4) & (filter5)]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True



    # Set up the matplotlib figure
    fig = plt.figure()

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(data=corr, mask=mask, annot=True, fmt='1.1f')
    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig


draw_cat_plot()
draw_heat_map()
