"""
3.) Write a function that takes a patient ID (string) as input and returns the mean inflammation level across the 40 days (float) for that given patient. Do not use any external libraries (such as numpy). Embed this function in a script called mean_inflammation.py that defines the patient ID as a variable, executes the function, and prints the output.
"""
import numpy as np

patient_id = 5
data = np.loadtxt('/Users/cmdb/data/bootcamp/python/inflammation-01.csv', dtype = int, delimiter = ',')
def mean_inflammation(patient_ID = int()) :
    patient_values = list(data[patient_ID, ])
    total = 0
    for i in range(len(patient_values)):
        total += patient_values[i]
    return total / len(patient_values)

print(mean_inflammation(5))
