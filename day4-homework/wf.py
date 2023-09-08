"""
Get a starting frequency and a population size

Input parameters for function

While our allele frequency is between 0 and 1:

    Get the new allele frequency for next generation by
    by drawing from binomial distribution
    (convert number of successes into a frequency)

    Store our allele frequency in the AF list


Return a list of allele frequencies at each time point
Number of generations to fixation is the length of the list
"""

import numpy as np
import matplotlib.pyplot as plt
np.random.seed(1234)
def wf(n = int(), p = float()):

    frequencies = [p]
    count = 0
    while 0 < frequencies[-1] < 1:
        counts = np.random.binomial(2*n, frequencies[count])
        freq = counts / (2*n)
        frequencies.append(freq)
        count +=1
    return frequencies

fig, ax = plt.subplots()

n = 12
p = 0.7

ax.plot(wf(n, p))
plt.xlabel("Generation Number")
plt.ylabel("Allele Frequency")
plt.tight_layout()

fixation_time = []
for i in range(1000):
    fixation_time.append(len(wf(n,p)))

fig2, ax2 = plt.subplots()

ax2.hist(fixation_time)
plt.xlabel("Generations until Fixation")
plt.ylabel("Count")
plt.tight_layout()


pop_sizes = [50, 60, 70, 80, 90]
avg_fix_times = []
for ps in pop_sizes:
    fix_times = []
    for i in range(50):
        n = ps
        fix_times.append(len(wf(n, p)))
    avg_fix_times.append(np.mean(fix_times))

fig3, ax3 = plt.subplots()
ax3.plot(pop_sizes, avg_fix_times)
plt.xticks(pop_sizes)
plt.xlabel("Number of Alleles in Population")
plt.ylabel("Mean Generation Number to Fixation \n over 50 Simulations")
plt.tight_layout()


afs = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
avg_fix_times = []
for p in afs:
    fix_times = []
    for i in range(1000):
        n = 1000
        fix_times.append(len(wf(n, p)))
    avg_fix_times.append(np.mean(fix_times))

fig4, ax4 = plt.subplots()
ax4.plot(afs, avg_fix_times)
plt.xticks(afs)
plt.xlabel("Initial Allele Frequency")
plt.ylabel("Mean Fixation Generation Number \n over 1000 Simulations (N = 10)")
plt.tight_layout()

plt.show()





