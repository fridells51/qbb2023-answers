import numpy as np
import pandas as pd
from pydeseq2 import preprocessing
from matplotlib import pyplot as plt
import seaborn as sns
# read in data
counts_df = pd.read_csv("gtex_whole_blood_counts_formatted.txt", index_col = 0)

# read in metadata
metadata = pd.read_csv("gtex_metadata.txt", index_col = 0)

# normalize
counts_df_normed = preprocessing.deseq2_norm(counts_df)[0]

# log
counts_df_logged = np.log2(counts_df_normed + 1)

# merge with metadata
full_design_df = pd.concat([counts_df_logged, metadata], axis=1)

#1.1 subject GTEX-113JC
gtex113jc = counts_df_logged.loc['GTEX-113JC'][counts_df_logged.loc['GTEX-113JC'] > 0]


plt.hist(gtex113jc, bins=30, color='blue', edgecolor='black')
plt.title(f'Distribution of Expression for GTEX-113JC')
plt.xlabel('Logged Normalized Counts')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()
plt.savefig('gtex113jc-expression.png')

#1.2 gene 'MXD4' 

expression_values_male = full_design_df[full_design_df['SEX'] == 1]['MXD4']
expression_values_female = full_design_df[full_design_df['SEX'] == 2]['MXD4']

plt.figure(figsize=(10, 6))
plt.hist(expression_values_male, bins=30, color='blue', alpha=0.7, label='Male', edgecolor='black')
plt.hist(expression_values_female, bins=30, color='pink', alpha=0.7, label='Female', edgecolor='black')
plt.title(f'Distribution of Expression for MXD4 in Males vs Females')
plt.xlabel('Logged Normalized Counts')
plt.ylabel('Frequency')
plt.legend()
plt.grid(True)
plt.show()
plt.savefig('mxd4-bysex.png')


metadata_subset = metadata[['AGE', 'DTHHRDY']]

pivot_table = metadata_subset.pivot_table(index='AGE', columns='DTHHRDY', aggfunc='size', fill_value=0)

pivot_table_percentage = pivot_table.div(pivot_table.sum(axis=1), axis=0)

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table_percentage, annot=True, cmap='coolwarm', fmt=".2%", cbar_kws={'label': 'Relative Proportion'})
plt.title('Relative Proportion of Subjects in Each Hardy Scale Category for Each Age Group')
plt.xlabel('Hardy Scale Category')
plt.ylabel('Age Group')
plt.show()
plt.savefig('hardy-scale-acrossage.png')


gene_data = full_design_df[['AGE', 'SEX', 'LPXN']]

median_expression = gene_data.groupby(['AGE', 'SEX'])['LPXN'].median().reset_index()
sex_labels = {1: 'Female', 2: 'Male'}
median_expression['SEX'] = median_expression['SEX'].map(sex_labels)
plt.figure(figsize=(12, 8))
sns.barplot(x='AGE', y='LPXN', hue='SEX', data=median_expression, ci=None)
plt.legend(title='Sex')
plt.title(f'Median Expression of LPXN Over Time Stratified by Sex')
plt.xlabel('Age Category')
plt.ylabel('Median Logged Normalized Counts')
plt.savefig('sex-stratified-with-age.png')
