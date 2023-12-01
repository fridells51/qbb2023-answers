import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('2018_Central_Park_Squirrel_Census_-_Squirrel_Data_20231201.csv', header=0)

# what are squirrels up to?
df_behavior = df.dropna(subset=['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging', 'Kuks', 'Quaas', 'Moans'])

behavior_counts = df_behavior[['Running', 'Chasing', 'Climbing', 'Eating', 'Foraging', 'Kuks', 'Quaas', 'Moans']].apply(pd.Series.value_counts)

plt.figure(figsize=(12, 8))
behavior_counts.T.plot(kind='bar', width=0.8, edgecolor='black')
plt.title('Distribution of Squirrel Behaviors')
plt.xlabel('Behavior')
plt.ylabel('Count')
plt.legend(title='Behavior', loc='upper right', bbox_to_anchor=(1.15, 1))
plt.tight_layout()
plt.savefig('behavior.png')
plt.close()
# Are squirrels flagging or twitching their tails?
df_tails = df.dropna(subset=['Tail flags', 'Tail twitches'])
behavior_counts = df_tails[['Tail flags', 'Tail twitches']].apply(pd.Series.value_counts)

plt.figure(figsize=(14, 10))
behavior_counts.T.plot(kind='bar', width=0.8, color=['blue', 'green'], edgecolor='black')
plt.title('Comparison of Tail Flags and Tail Twitches in Squirrels')
plt.xlabel('Behavior')
plt.ylabel('Count')
plt.legend(title='Tail Behavior')
plt.tight_layout()
plt.savefig('tail_behavior.png')
plt.close()
# plot spatial distribution colored by fur color
fur_df = df.dropna(subset=['Primary Fur Color'])

fur_df.loc[:, 'Primary Fur Color'] = fur_df['Primary Fur Color'].replace('Cinnamon', 'Brown')

colors = fur_df['Primary Fur Color'].map({'Gray': 'gray', 'Brown': 'brown', 'Black': 'black'})

plt.figure(figsize=(12, 8))
plt.scatter(fur_df['X'], fur_df['Y'], c=colors, alpha=0.5)
plt.title('Spatial Distribution of Squirrels Colored by Their Fur Color')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

legend_labels = {'gray': 'Gray', 'brown': 'Brown', 'black': 'Black'}
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10, label=label) for color, label in legend_labels.items()]
plt.legend(handles=legend_handles, title='Fur Color')
plt.savefig('spatial-colored-squirrels.png')
plt.close()
