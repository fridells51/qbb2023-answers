import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

"""
Step 1.2

Simulate sequencing of 3x coverage of a 1Mbp genome
with 100 bp reads

"""

def simulate_coverage(cov, size, read, figname):

    coverage_array = np.zeros(size)

    sims = int(cov * size / read)

    starts = np.random.randint(0, size-read+1, size = sims)

    for start in starts:
        coverage_array[start: start + read] += 1

    x = np.arange(0, max(coverage_array)+1)

    sim_0cov = size - np.count_nonzero(coverage_array)

    print(f'In the simulation, there are {sim_0cov} bases with a coverage of 0')

    percent_0 = 100 * sim_0cov/size

    print(f'This is {percent_0}% of the genome')

    fig, ax = plt.subplots()

    pois = stats.poisson.pmf(x, mu = cov) * size

    norm = stats.norm.pdf(x, cov, cov**0.5) * size

    ax.hist(coverage_array, bins = x, align='left', label = 'Simulation')
    ax.plot(x, pois, color = 'red', label = 'Poisson Distribution')
    ax.plot(x, norm, color = 'green', label = 'Normal Distribution')
    ax.set_xlabel('Coverage')
    ax.set_ylabel('Count')
    ax.legend()
    fig.tight_layout()
    fig.savefig(figname)

simulate_coverage(3, 1000000, 100, 'ex1_3x_cov.png')
simulate_coverage(10, 1000000, 100, 'ex1_10x_cov.png')
simulate_coverage(30, 1000000, 100, 'ex1_30x_cov.png')

"""
Exercise 2: DBG Construction
"""

reads = ['ATTCA', 'ATTGA', 'CATTG', 'CTTAT', 'GATTG', 'TATTT', 'TCATT', 'TCTTA', 'TGATT', 'TTATT', 'TTCAT', 'TTCTT', 'TTGAT']

with open('dbg_2-1.txt', 'w') as writefile:
    writefile.write('digraph { ')
    for read in reads:
        writefile.write(read[0:3] + ' -> ' + read[1:4] + ';\n')
        writefile.write(read[1:4] + ' -> ' + read[2:] + ';\n')
    writefile.write(' }')

writefile.close()



