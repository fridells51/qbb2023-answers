import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats import multitest
from pydeseq2 import preprocessing
from pydeseq2.dds import DeseqDataSet
from pydeseq2.ds import DeseqStats
import csv
## read in data
counts_df = pd.read_csv("gtex_whole_blood_counts_formatted.txt", index_col = 0)
#
## read in metadata
metadata = pd.read_csv("gtex_metadata.txt", index_col = 0)
#
## Normalize
counts_df_normed = preprocessing.deseq2_norm(counts_df)[0]
#
## log transform
counts_df_normed = np.log2(counts_df_normed + 1)
#
## Create design matrix
#
full_design_df = pd.concat([counts_df_normed, metadata], axis=1)
#
# Example with one gene

#output = 'DE_results.csv'
#
#with open(output, 'w') as wf:
#    writer = csv.writer(wf)
#    writer.writerow(['Gene', 'Slope', 'P'])
#    de_results = {}
#    for col in full_design_df.columns:
#        if col != 'SEX':
#            model = smf.ols(formula = f'Q("{col}") ~ SEX', data=full_design_df)
#            results = model.fit()
#            writer.writerow([col, results.params['SEX'], results.pvalues['SEX']])
#        else:
#            break
#    wf.close()
#
de = pd.read_csv('DE_results.csv')
de['P'] = de['P'].fillna(1.0)
q_vals = multitest.fdrcorrection(de['P'], alpha=0.05, method='indep', is_sorted=False)
de['Q'] = q_vals[1]

filtered = de[de['Q']<=0.1]
filtered.to_csv('FDR_Controlled_genes.tsv', sep='\t')

dds = DeseqDataSet(
    counts=counts_df,
    metadata=metadata,
    design_factors="SEX"
)

dds.deseq2()
stat_res = DeseqStats(dds)
stat_res.summary()
results = stat_res.results_df
results.to_csv('deseq_results.tsv', sep = '\t')

# filter these at the padj < 0.1 level

des = pd.read_csv('deseq_results.tsv', index_col = 0, delimiter = '\t')
des['padj'] = des['padj'].fillna(1.0)
filtered_deseq = des[des['padj']<=0.1]
filtered_deseq.to_csv('filtered_deseq.tsv', sep = '\t')

# compute jaccard
intersection = filtered_deseq.index.intersection(filtered['Gene'])
union = filtered_deseq.index.union(filtered['Gene'])

jaccard_index = len(intersection) / len(union) * 100

import matplotlib.pyplot as plt
# thresholds for plotting
fdr_threshold = 0.1
log2foldchange_threshold = 1.0
plt.figure(figsize=(10, 6))
plt.scatter(filtered_deseq['log2FoldChange'], -np.log10(filtered_deseq['padj']), color='grey', alpha=0.5)
significant_genes = filtered_deseq[(filtered_deseq['padj'] <= fdr_threshold) & (abs(filtered_deseq['log2FoldChange']) > log2foldchange_threshold)]
plt.scatter(significant_genes['log2FoldChange'], -np.log10(significant_genes['padj']),
            color='red', label='Significant Genes')

plt.xlabel('log2FoldChange')
plt.ylabel('-log10(padj)')
plt.title('Volcano Plot')
plt.legend()
plt.savefig('volcano_plot.png')
