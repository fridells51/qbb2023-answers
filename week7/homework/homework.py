import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def read_bedgraph(file_path):
    sites = set()
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            chromosome, start, stop = parts[0], int(parts[1]), int(parts[2])
            sites.add((chromosome, start, stop))
    return sites

def calculate_statistics(file_a_sites, file_b_sites):
    only_in_a = file_a_sites - file_b_sites
    only_in_b = file_b_sites - file_a_sites
    shared_sites = file_a_sites.intersection(file_b_sites)

    total_sites = len(file_a_sites.union(file_b_sites))
    shared_percentage = (len(shared_sites) / total_sites) * 100

    return len(only_in_a), len(only_in_b), len(shared_sites), shared_percentage

ont_path = 'ONT.cpg.chr2.bedgraph'
bisulfite_path = 'bisulfite.cpg.chr2.bedgraph'

ont_sites = read_bedgraph(ont_path)
bisulfite_sites = read_bedgraph(bisulfite_path)

only_in_ont, only_in_bisulfite, shared_sites, shared_percentage = calculate_statistics(ont_sites, bisulfite_sites)


def read_bedgraph_coverage(file_path):
    coverages = []
    with open(file_path, 'r') as file:
        for line in file:
            fields = line.strip().split('\t')
            coverage = int(fields[4])
            coverages.append(coverage)
    return coverages



def plot_coverage_distributions(paths):
    labels = ['ONT', 'Bisulfite']
    ont_coverages = read_bedgraph_coverage(paths[0])
    ont_coverages, ont_counts = np.unique(ont_coverages, return_counts=True)
    plt.bar(ont_coverages, ont_counts, alpha=0.5, label=labels[0])
    bis_coverages = read_bedgraph_coverage(paths[1])
    bis_coverages, bis_counts = np.unique(bis_coverages, return_counts=True)
    plt.bar(bis_coverages, bis_counts, alpha=0.5, label=labels[1])
    plt.title('Distribution of Coverages Across CpG Sites')
    plt.xlabel('Coverage')
    plt.xlim(0,100)
    plt.ylabel('Frequency')
    plt.legend()
    plt.savefig('coverage.png')
    plt.show()
    plt.close()

def bedgraph_pd(file_path):
    columns = ['chromosome', 'start', 'stop', 'methylation', 'coverage']
    return pd.read_csv(file_path, sep='\t', header=None, names=columns)

def merge_bedgraphs(ont_file, bis_file):
    df_ont = bedgraph_pd(ont_file)
    df_bis = bedgraph_pd(bis_file)

    merged_data = pd.merge(df_ont, df_bis, on=['chromosome', 'start', 'stop'], suffixes=('_ont', '_bis'), how='inner')

    return merged_data

def calculate_pearson_r(methylation_ont, methylation_bis):
    return np.corrcoef(methylation_ont, methylation_bis)[0, 1]

def plot_2d_histogram(methylation_ont, methylation_bis):
    histogram, x_edges, y_edges = np.histogram2d(methylation_ont, methylation_bis, bins=100)
    histogram = np.log10(histogram + 1)  # Log transformation

    plt.imshow(histogram, extent=[x_edges[0], x_edges[-1], y_edges[0], y_edges[-1]], cmap='viridis', aspect='auto')
    plt.colorbar(label='log10(Count + 1)')
    plt.xlabel('Methylation Score ONT')
    plt.ylabel('Methylation Score Bisulfite')




merged_data = merge_bedgraphs(ont_path, bisulfite_path)

methylation_ont = merged_data['methylation_ont']
methylation_bisulfite = merged_data['methylation_bis']

plot_2d_histogram(methylation_ont, methylation_bisulfite)
pearson_r = calculate_pearson_r(methylation_ont, methylation_bisulfite)
plt.title(f'2D Histogram of Methylation Scores\nPearson R: {pearson_r:.3f}')
plt.savefig('2dhist.png')
plt.show()
plt.close()


plot_coverage_distributions([ont_path, bisulfite_path])

import seaborn as sns

def merge_TN_bedgraphs(normal_path, tumor_path):
    normal_data = bedgraph_pd(normal_path)
    tumor_data = bedgraph_pd(tumor_path)

    merged_TN_data = pd.merge(normal_data, tumor_data, on=['chromosome', 'start', 'stop'], suffixes=('_normal', '_tumor'), how='inner')

    return merged_TN_data

def calculate_methylation_changes(df):
    df['methylation_change'] = df['methylation_tumor'] - df['methylation_normal']
    df = df[df['methylation_change'].notna()]  # Exclude values with no change

    return df

def plot_violin(methylation_change_common):

    sns.violinplot(x='approach', y='methylation_change', data=methylation_change_common)

    plt.xlabel('Sequencing Type')
    plt.ylabel('Methylation Change (Tumor - Normal)')
    plt.title('Distribution of Methylation Changes for Common Sites')

def calculate_pearson_r(methylation_change_common):
    nanopore_data = methylation_change_common[methylation_change_common['approach'] == 'Nanopore']
    bisulfite_data = methylation_change_common[methylation_change_common['approach'] == 'Bisulfite']

    pearson_r = np.corrcoef(
        nanopore_data['methylation_change'],
        bisulfite_data['methylation_change']
    )[0, 1]

    return pearson_r

normal_nano_path = 'normal.ONT.chr2.bedgraph'
tumor_nano_path = 'tumor.ONT.chr2.bedgraph'
normal_bisulfite_path = 'normal.bisulfite.chr2.bedgraph'
tumor_bisulfite_path = 'tumor.bisulfite.chr2.bedgraph'

merged_data_nano = merge_TN_bedgraphs(normal_nano_path, tumor_nano_path)
merged_data_bisulfite = merge_TN_bedgraphs(normal_bisulfite_path, tumor_bisulfite_path)

common_sites = set(merged_data_nano.index).intersection(merged_data_bisulfite.index)

methylation_change_nanopore = calculate_methylation_changes(merged_data_nano.loc[list(common_sites)])
methylation_change_bisulfite = calculate_methylation_changes(merged_data_bisulfite.loc[list(common_sites)])

methylation_change_nanopore['approach'] = 'Nanopore'
methylation_change_bisulfite['approach'] = 'Bisulfite'

methylation_change_common = pd.concat([methylation_change_nanopore, methylation_change_bisulfite], ignore_index=True)

plot_violin(methylation_change_common)

pearson_r = calculate_pearson_r(methylation_change_common)
plt.title(f'Distribution of Methylation Changes\nPearson R: {pearson_r:.3f}')
plt.savefig('violin_plots.png')
plt.show()
plt.close()
