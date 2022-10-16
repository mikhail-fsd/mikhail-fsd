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



# sns.catplot([0, 1, 2, 3, 4, 5])
# plt.show()

df_melt_cardio = df.melt(id_vars=['cardio'], value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])
#df_cardio_0 = df_melt_cardio[df_melt_cardio['cardio'] == 0].sort_values(by=['value', 'variable'])
#df_cardio_1 = df_melt_cardio[df_melt_cardio['cardio'] == 1]
#df_cat0 = df_cardio_0.groupby('variable')
#df_df = df_cat0['value'].value_counts()
#sns.countplot(data=df_cardio_0, x='variable', hue='value')
#plt.show()
print(df_melt_cardio)
df_by_cardio = df_melt_cardio.groupby('cardio')
sns.catplot(data=df_melt_cardio, x='variable', hue='value', col='cardio', kind='count').set(ylabel='total')

plt.show()

#print(df_by_cardio.get_group(0)['value'].value_counts())



# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat1 = None


    # Group and reformat the data to split it by 'cardio'. Show the counts of each feature. You will have to rename one of the columns for the catplot to work correctly.
    df_cat = None
    

    # Draw the catplot with 'sns.catplot()'



    # Get the figure for the output
    fig = None


    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = None

    # Calculate the correlation matrix
    corr = None

    # Generate a mask for the upper triangle
    mask = None



    # Set up the matplotlib figure
    fig, ax = None

    # Draw the heatmap with 'sns.heatmap()'



    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
