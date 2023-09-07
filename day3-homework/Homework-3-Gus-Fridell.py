#!/usr/bin/env python

"""
1.) Without using any external libraries (such as numpy) write a function that takes a list (of any length) of integers as input and returns the mean (i.e., average). Write a script called mean.py where you create the list of integers, compute the mean using your function, and print it.

2.) Use the function from part 1 to write a Python script called mean_from_file.py that computes and prints the mean of a series of integers from a data file (e.g., “my_integers.txt”) where the data contain a set of integers, one per line. [Optional: Write your code so that the user can specify the name of that file from the command line (hint: use sys.argv).]

Extend the Day-1 homework without using any external libraries (such as numpy) unless otherwise noted to analyze data from inflammation.csv:

3.) Write a function that takes a patient ID (string) as input and returns the mean inflammation level across the 40 days (float) for that given patient. Do not use any external libraries (such as numpy). Embed this function in a script called mean_inflammation.py that defines the patient ID as a variable, executes the function, and prints the output.

4.) Write a function that takes two patient IDs (strings) as input and returns a list of the difference between their inflammation levels on each of the 40 days (floats). Embed this function in a script called difference_inflammation.py that defines the patient IDs as variables, executes the function, and prints the output.
"""

# Question 1


def mean(input_list = list()):
# Add to a sum iteratively
    total = 0
    for i in range(len(input_list)):
        if isinstance(input_list[i], int) or isinstance(input_list[i], float):
            total += input_list[i]
        else:
            print(f'Data type in the list must be numeric')
            total = None
            break
    if total == None:
        return
    if len(input_list) > 0:
        return total / len(input_list)
    else:
        print(f'Length of list is 0 and the average cannot be computed')
        return



# Question 2 (refer to mean_from_file.py)


# Question 3 (refer to mean_inflammation.py)



