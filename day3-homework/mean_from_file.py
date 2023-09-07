"""
2.) Use the function from part 1 to write a Python script called mean_from_file.py that computes and prints the mean of a series of integers from a data file (e.g., “my_integers.txt”) where the data contain a set of integers, one per line. [Optional: Write your code so that the user can specify the name of that file from the command line (hint: use sys.argv).]
"""

import sys

def mean_from_file(data = sys.argv[1]):
    numbers = []
    for line in open(data, 'r'):
        numbers.append(int(line))
    total = 0

    for i in numbers:
        total += i
    return total / len(total)



