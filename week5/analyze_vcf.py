import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Read VCF

r_depth = []
g_qual = []
af_spec = []
effect = []
for line in open('hw-data/ann_decomposed.vcf'):
    if line.startswith('#'):
        continue
    fields = line.rstrip('\n').split('\t')
    samples = fields[9:]
    # DP field is the one we're after for read depths
    for s in samples:
        if s.split(':')[2] != '.':
            dp = r_depth.append(float(s.split(':')[2]))
        # GQ for genotype quality
        if s.split(':')[1] != '.':
            gq = g_qual.append(float(s.split(':')[1]))
    # allele_freq is field 4 in the INFO field
    for j in fields[7].split(';')[3].split('=')[1].split(','):
        af_spec.append(float(j))
    # Get the first field of the ann field
    if fields[7].split('ANN=')[1].split('|')[1] != '':
        effect.append(fields[7].split('ANN=')[1].split('|')[1])



# Make the plots

fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Plot histograms in each subplot
axs[0, 0].hist(r_depth, color='blue', alpha=0.7, label='Read Depth')
axs[0, 1].hist(g_qual, color='green', alpha=0.7, label='Genotype Quality')
axs[1, 0].hist(af_spec, color='red', alpha=0.7, label='Allele Frequency')

# Set titles and labels for each subplot
axs[0, 0].set_title('DIstribution of Read Depth')
axs[0, 1].set_title('Distribution of Genotype Quality')
axs[1, 0].set_title('Per-site Allele Frequency')

unique_values = np.unique(effect)
colors = plt.cm.viridis(np.linspace(0, 1, len(unique_values)))
for ind, val in enumerate(unique_values):
    count = effect.count(val)
    axs[1, 1].bar(val, count, color = colors[ind], label=val)

axs[1, 1].tick_params(axis='x', labelrotation=90)
labels = ['Read Depth', 'Genotype Quality', 'Allele Frequency', 'Effect']
for i, ax in enumerate(axs.flat):
    xlabl = labels[i]
    ax.set(xlabel=xlabl, ylabel='Frequency')

# Adjust spacing between subplots
plt.tight_layout()

plt.savefig('vcf_histograms.png')
