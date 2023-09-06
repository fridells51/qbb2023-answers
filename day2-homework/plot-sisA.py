#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# Get dataset to recreate Fig 3B from Lott et al 2011 PLoS Biology https://pubmed.gov/21346796
# wget https://github.com/bxlab/cmdb-quantbio/raw/main/assignments/lab/bulk_RNA-seq/extra_data/all_annotated.csv
# sisA (FBtr0073461)

#Modify plot-sisA.py (do not create a new file) to load the transcripts information using open() and a for loop rather than np.loadtxt(). Remember that the first line is a header and should not be stored in the transcripts list. Push just your code to your git repository and confirm at https://github.com that your code no longer uses np.loadtxt().

transcripts = []
for line in open("all_annotated.csv", 'r'):
    if line.startswith("t_name"):
        continue
    else:
        transcripts.append(line.split(',')[0])

#transcripts = np.loadtxt( "all_annotated.csv", delimiter=",", usecols=0, dtype="<U30", skiprows=1 )
print( "transcripts: ", transcripts[0:5] )

samples = np.loadtxt( "all_annotated.csv", delimiter=",", max_rows=1, dtype="<U30" )[2:]
print( "samples: ", samples[0:5] )

data = np.loadtxt( "all_annotated.csv", delimiter=",", dtype=np.float32, skiprows=1, usecols=range(2, len(samples) + 2) )
print( "data: ", data[0:5, 0:5] )

# Find row with transcript of interest
row = None
for i in range(len(transcripts)):
    if transcripts[i] == 'FBtr0073461':
        row = i

# Separate the Male and Female data visually on the plot

full_expression = data[row, ]
m_expr = []
f_expr = []
for i in range(len(samples)):
    if samples[i].startswith("male"):
        m_expr.append(full_expression[i])
    else:
        f_expr.append(full_expression[i])

dev_samples = set()
for i in range(len(samples)):
    dev_samples.add(samples[i].split('_')[1])

# Combine the m_expr and f_expr into an array
combined = np.array([f_expr, m_expr])


# Prepare data
x = sorted(list(dev_samples))
y1 = f_expr
y2 = m_expr

# Plot data
fig, ax = plt.subplots()
ax.set_title( "FBtr0073461" )
ax.plot( x, y1 , label = 'Female')
ax.plot( x, y2 , label = 'Male')
plt.ylabel("mRNA Abundance (RPKM)")
plt.xlabel("developmental stage")
plt.xticks(rotation=90)
plt.legend()
fig.set_tight_layout(True)
fig.savefig( "FBtr0073461.png" )
plt.close( fig )
