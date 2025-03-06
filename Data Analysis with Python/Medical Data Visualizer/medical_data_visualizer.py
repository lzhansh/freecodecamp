import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# 1
df = pd.read_csv("medical_examination.csv")

# 2
df['overweight'] = np.where (df.weight / (df.height * 0.01)**2 > 25 , 1 , 0)

# 3
df['cholesterol'] = np.where( df['cholesterol'] == 1 , 0 , 1)
df['gluc'] = np.where(df['gluc'] == 1 , 0 , 1)

# 4
def draw_cat_plot():
    # 5
    df_cat = pd.melt(df, ['cardio'], ['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])


    # 6
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')
    

    # 7
    catplot = sns.catplot(df_cat, x='variable', y= 'total', hue='value', col='cardio', 
             kind='bar', height=5, aspect=1.2)

    # 8
    fig = catplot.fig

    # 9
    fig.savefig('catplot.png')
    return fig


# 10
def draw_heat_map():
    # 11
    df_heat = df[(df['ap_lo'] <= df['ap_hi']) 
            & (df['height'] >= df['height'].quantile(0.025)) 
            & (df['height'] <= df['height'].quantile(0.975))
            & (df['weight'] >= df['weight'].quantile(0.025)) 
            & (df['weight'] <= df['weight'].quantile(0.975))]

    # 12
    corr = df_heat.corr().round(1)

    # 13
    mask = np.triu(np.ones(corr.shape, dtype=bool))

    # 14
    fig, ax = plt.subplots(figsize = (8,6))

    # 15
    sns.heatmap(corr, mask = mask, annot=True, fmt=".1f")

    # 16
    fig.savefig('heatmap.png')
    return fig
