#!/usr/bin/env python


# Read in the contents of the file, line by line
contents = [line.rstrip() for line in open('data/inflammation-01.csv')]

# Separate the rows into lists, and evaluate them as ints

data = [contents[i].split(',') for i in range(len(contents))]

fixed_data = []

for i in range(len(data)):
    fixed_data.append([eval(j) for j in data[i]])

"""
Exercise 1

Print the number of flare-ups that the fifth patient had on the first, tenth, and last day
"""

flare_ups = [fixed_data[4][0], fixed_data[4][9], fixed_data[4][-1]]

print(flare_ups)

"""
Exercise 2:

For each patient, calculate the average number of flare-ups per day. Print the average values for the first 10 patients.

These are the row averages - for example, patient 1 has 5.45 flare-ups per day on average; patient 2 has 5.425 flare-ups per day on average.
"""

patient_averages = []

for data in fixed_data:
    patient_averages.append(sum(data)/len(data))

print(patient_averages[:9])

"""
Exercise 3:

Using the average flare-ups per day calculated in part 2, print the highest and lowest average number of flare-ups per day.
"""

highest = max(patient_averages)
lowest = min(patient_averages)

print("The highest number of flare-ups per day is " + str(highest))
print("The lowest number of flare-ups per day is " + str(lowest))

"""
Exercise 4:

For each day, print the difference in number of flare-ups between patients 1 and 5
"""

diff_1_5 = []

zipper = zip(fixed_data[0], fixed_data[4])
for pat1_i, pat2_i in zipper:
    diff_1_5.append(pat1_i - pat2_i)


print(diff_1_5)

