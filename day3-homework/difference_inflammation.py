"""
4.) Write a function that takes two patient IDs (strings) as input and returns a list of the difference between their inflammation levels on each of the 40 days (floats). Embed this function in a script called difference_inflammation.py that defines the patient IDs as variables, executes the function, and prints the output.
"""


import numpy as np

patient_id = 5
patient_id2 = 6
data = np.loadtxt('/Users/cmdb/data/bootcamp/python/inflammation-01.csv', dtype = int, delimiter = ',')

def difference(patient_id = int(), patient_id2 = int()):
    patient_values1 = list(data[patient_id, ])
    patient_values2 = list(data[patient_id2, ])
    zipper = zip(patient_values1, patient_values2)
    diff = []
    for pat1, pat2 in zipper:
        diff.append(pat1 - pat2)
    return diff

print(difference(5, 6))
