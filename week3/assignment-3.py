import numpy as np
from fasta import readFASTA
import sys
import pandas as pd
"""
Write a script to perform global alignment between two sequences using a given scoring matrix and gap penalty. Your script will take four inputs:

    A FASTA-style file containing two sequences to align
    A text file containing the scoring matrix you’d like to use for this alignment
    The penalty for gaps in your alignment (so if users wanted to penalize gaps by subtracting 10 from the alignment score, they would input -10)
    The filepath to write your alignment to
"""


def needleman_wunsch(reads, scoring_matrix, gap_penalty):
    gap_penalty = int(gap_penalty)
    #read inputs and convince pandas not to SUCK
    input_sequences = readFASTA(open(reads))
    scoring_matrix = pd.read_csv(scoring_matrix, index_col=0, header = 0, delim_whitespace=True)
    sequence1_id, sequence1 = input_sequences[0]
    sequence2_id, sequence2 = input_sequences[1]
    sequence1 = 'TACGATTA'
    sequence2 = 'ATTAACTTA'
    m, n = len(sequence1), len(sequence2)
    F = np.zeros((m+1, n+1))
    traceback = np.zeros((m + 1, n + 1), dtype=int)

    # first row and column have set values
    # So for traceback idrk what values to use. I need left diag and up
    for i in range(m + 1):
        F[i][0] = gap_penalty * i
        traceback[i][0] = 1
    for j in range(n + 1):
        F[0][j] = gap_penalty * j
        traceback[0][j] = 2

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            substitution = F[i - 1][j - 1] + scoring_matrix.at[sequence1[i - 1], sequence2[j - 1]]
            deletion = F[i - 1][j] + gap_penalty
            insertion = F[i][j - 1] + gap_penalty
            F[i][j] = max(substitution, deletion, insertion)

            # Update the traceback matrix
            if F[i][j] == substitution:
                traceback[i][j] = 0
            elif F[i][j] == deletion:
                traceback[i][j] = 2
            else:
                traceback[i][j] = 1

    traceback_aln1, traceback_aln2 = "", ""
    h, k = m, n
    print(h)
    print(k)
    while h > 0 or k > 0:
        if traceback[h][k] == 0:
            traceback_aln1 = sequence1[h - 1] + traceback_aln1
            traceback_aln2 = sequence2[k - 1] + traceback_aln2
            h -= 1
            k -= 1
        elif traceback[h][k] == 1:
            traceback_aln1 = sequence1[h - 1] + traceback_aln1
            traceback_aln2 = "-" + traceback_aln2
            h -= 1
        else:
            traceback_aln1 = "-" + traceback_aln1
            traceback_aln2 = sequence2[k - 1] + traceback_aln2
            k -= 1

    return traceback_aln1, traceback_aln2, F[m][n]


fasta = sys.argv[1]
scoring_matrix = sys.argv[2]
gap_penalty = int(sys.argv[3])
output_file = sys.argv[4]

alignment1, alignment2, alignment_score = needleman_wunsch(sys.argv[1], sys.argv[2], sys.argv[3])

num_gaps_sequence1 = alignment1.count("-")
num_gaps_sequence2 = alignment2.count("-")

with open(output_file, 'w') as outfile:
    outfile.write(f">Sequence 1\n{alignment1}\n")
    outfile.write(f">Sequence 2\n{alignment2}\n")

print(f"Number of gaps in Sequence 1: {num_gaps_sequence1}")
print(f"Number of gaps in Sequence 2: {num_gaps_sequence2}")
print(f"Alignment Score: {alignment_score}")
