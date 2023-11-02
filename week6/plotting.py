import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



data = np.loadtxt('top2pcs')

plt.figure(figsize=(8, 6))
plt.scatter(data[:, 0], data[:, 1], s=10, alpha=0.5)
plt.title("PCA Plot - PC1 vs. PC2")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.grid(True)
plt.show()
plt.close()

afdata = np.loadtxt("allele_frequencies.txt", usecols=(1,))

plt.figure(figsize=(8, 6))
plt.hist(afdata, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
plt.title("Allele Frequency Histogram")
plt.xlabel("Allele Frequency")
plt.ylabel("Frequency Count")

plt.xlabel("Allele Frequency")
plt.ylabel("Frequency Count")


plt.grid(True)

plt.show()
plt.close()

gwas_results_CB = pd.read_csv("CB_gwas_results.assoc.linear", delim_whitespace = True)

gwas_results_GS = pd.read_csv("GS_gwas_results.assoc.linear", delim_whitespace = True)

fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

def highlight_significant_snps(data, ax):
    significant_snps = data[data['P'] < 1e-5]
    ax.scatter(significant_snps.index, -1 * np.log(significant_snps['P']), color='red', label='p < 1e-5', zorder=5)
    ax.legend(loc='upper right')

axes[0].scatter(gwas_results_CB.index, -1 * np.log(gwas_results_CB['P']), s=5, color='blue')
highlight_significant_snps(gwas_results_CB, axes[0])
axes[0].set_title('Manhattan Plot - CB')
axes[0].set_xlabel('SNP Index')
axes[0].set_ylabel('-log10(p-value)')

axes[1].scatter(gwas_results_GS.index, -1 * np.log(gwas_results_GS['P']), s=5, color='blue')
highlight_significant_snps(gwas_results_GS, axes[1])
axes[1].set_title('Manhattan Plot - GS')
axes[1].set_xlabel('SNP Index')
axes[1].set_ylabel('-log10(p-value)')

plt.tight_layout()
plt.savefig('manhattan_plots.png')
plt.show()
plt.close()
# plot the effect size of the most significant variant with boxplot of phenotype stratified by genotype

# Get the ID of the SNP with the lowest P-value

min_p_index = gwas_results_CB['P'].idxmin()
rsid = gwas_results_CB['SNP'][min_p_index]
sample_phenotypes = pd.read_csv('gwas_data/CB1908_IC50.txt', delim_whitespace= True)
phe_vals = sample_phenotypes.iloc[:,2]
hom_ref = []
het = []
hom_alt = []

for line in open('gwas_data/genotypes.vcf'):
    if line.startswith('#'):
        continue
    fields = line.rstrip('\n').split('\t')
    if fields[2] == rsid:
        print(rsid)
        samples = fields[9:]
        for i in range(len(samples)):
            if samples[i] == '0/0':
                if not np.isnan(phe_vals[i]):
                    hom_ref.append(phe_vals[i])
            if samples[i] == '0/1' or samples[i] == '1/0':
                if not np.isnan(phe_vals[i]):
                    het.append(phe_vals[i])
            if samples[i] == '1/1':
                if not np.isnan(phe_vals[i]):
                    hom_alt.append(phe_vals[i])

        break

strat = [hom_ref, het, hom_alt]

gts = ['hom_ref', 'het', 'hom_alt']

plt.boxplot(strat, labels = gts)
plt.xlabel('Genotype')
plt.ylabel('Phenotype Score')
plt.title(f'CB Phenotype Score by {rsid} Genotype')
plt.savefig('boxplot.png')
plt.show()
plt.close()


