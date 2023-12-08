#!/usr/bin/env python

import sys

import scanpy as sc
import numpy
import matplotlib.pyplot as plt


adata = sc.read_h5ad("variable_data.h5")
adata.uns['log1p']['base'] = None

# 1.1
sc.pp.neighbors(adata, n_neighbors = 10, n_pcs = 40)


# 1.2
sc.tl.leiden(adata)

# 1.3
sc.tl.umap(adata, maxiter = 900)
sc.tl.tsne(adata)

fig, ax = plt.subplots(ncols=2)
sc.pl.umap(adata, color = 'leiden', title = 'UMAP', show = False, ax = ax[0])
sc.pl.tsne(adata, color = 'leiden', title = 't-SNE', show = False, ax = ax[1])
plt.tight_layout()
plt.savefig('dimension-reduction.png')
plt.close(fig)


adata_copy = adata.copy()
wilcoxon_adata = sc.tl.rank_genes_groups(adata_copy, groupby='leiden', method='wilcoxon', use_raw=True, copy=True)

logreg_adata = sc.tl.rank_genes_groups(adata_copy, groupby='leiden', method='logreg', use_raw=True, copy=True)

sc.pl.rank_genes_groups(wilcoxon_adata, n_genes=25, title='Wilcoxon Rank-sum', sharey=False, show=False, use_raw=True)
plt.tight_layout()
plt.savefig('wilcoxon_ranking_plot.png')
plt.close()

sc.pl.rank_genes_groups(logreg_adata, n_genes=25, title='Logistic Regression', sharey=False, show=False, use_raw=True)
plt.tight_layout()
plt.savefig('logreg_ranking_plot.png')
plt.close()

leiden = adata.obs['leiden']
umap = adata.obsm['X_umap']
tsne = adata.obsm['X_tsne']
adata = sc.read_h5ad('filtered_data.h5')
adata.obs['leiden'] = leiden
adata.obsm['X_umap'] = umap
adata.obsm['X_tsne'] = tsne


marker_genes = ['PPBP', 'MS4A1', 'NKG7']

sc.tl.umap(adata_copy)
sc.pl.umap(adata_copy, color=marker_genes, use_raw=False)

num_genes = len(marker_genes)
fig, axes = plt.subplots(1, num_genes, figsize=(5*num_genes, 4))

for i, gene in enumerate(marker_genes):
    sc.pl.umap(adata, color=gene, ax=axes[i], show=False, legend_loc='on data', legend_fontsize=10, title=gene)


fig.suptitle('Expression of Marker Genes in UMAP')
plt.tight_layout()
fig.savefig('marker_genes_umap.png')
plt.close(fig)


cell_types = {
    '7': 'Megakaryocyte',
    '2': 'C-cells',
    '4': 'NK-cells',
}

adata_copy.obs['leiden'] = adata_copy.obs['leiden'].map(cell_types)

sc.tl.umap(adata_copy)

sc.pl.umap(adata_copy, color='leiden', legend_loc='on data', legend_fontsize=10, title='Overall Cell Types')

plt.savefig('overall_umap_cell_types.png')
plt.close()

