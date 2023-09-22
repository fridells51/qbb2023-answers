#!/usr/bin/python

import pandas as pd
import numpy as np


d1 = pd.read_csv('aau1043_dnm.csv')

"""
 You first want to count the number of paternally and
maternally inherited DNMs in each proband. Using this
dataframe, create a dictionary where the keys are the
proband IDs and the value associated with each key is
a list of length 2, where the first element in the list
is the number of maternally inherited DNMs and the
second element in the list is the number of paternally
inherited DNMs for that proband. You can ignore DNMs
without a specified parent of origin.

For example, let’s say your data had two probands with
IDs 675 and 1097. And let’s say proband 675 has 19
maternal DNMs and 51 paternal DNMs, and proband 1097 has
12 maternal DNMs and 26 paternal DNMs. Your final
dictionary would look like this:

{675 : [19, 51],
 1097 : [12, 26]}
"""

# Since we are ignoring DNMs without a specified parent
# let's subset the dataframe to only include rows where
# the parental ID is not something called nan
# Surely this will be something normal looking

d1_parents = d1[~pd.isna(d1.iloc[:,5])]

# Wow! =D

dic_parental = dict()
keylist = d1_parents.iloc[:,4]

for key in keylist:
    dic_parental[key] = [0,0]

# Let's count the co-ocurrences of each proband, parent

co_occur = pd.Series(list(zip(d1_parents.Proband_id,
                              d1_parents.Phase_combined
                              ))).value_counts()

for i in range(len(co_occur)):
    proband, parent = co_occur.index[i]
    if parent == 'mother':
        dic_parental[proband][0] = co_occur.iloc[i]
    else:
        dic_parental[proband][1] = co_occur.iloc[i]

"""
Step 1.3

Use the following code snippet to convert this dictionary into a new pandas
dataframe (this assumes your dictionary from step 1.2 is called deNovoCount):

deNovoCountDF = pd.DataFrame.from_dict(deNovoCount, orient = 'index', columns
= ['maternal_dnm', 'paternal_dnm'])

Feel free to ask questions about how this code is working or, if you’re
interested, you can try to figure it out yourself.
"""

deNovoCountDF = pd.DataFrame.from_dict(dic_parental, orient = 'index', columns
= ['maternal_dnm', 'paternal_dnm'])


"""
Step 1.4

Now, load the data from aau1043_parental_age.csv into a new pandas dataframe.

    HINT: You will probably want to use the index_col argument with
    pd.read_csv(). It will make your life easier in the next step.
"""

d2 = pd.read_csv('aau1043_parental_age.csv', index_col=0)

"""
Step 1.5

You now have two dataframes with complementary information. It would be nice to
have all of this in one data structure. Use the pd.concat() function (more
here) to combine your dataframe from step 3 with the dataframe you just created
in step 4 to create a new merged dataframe.

HINT: You will want to specify the axis and join arguments with pd.concat()
"""

df_full = pd.concat([d2, deNovoCountDF], axis=1)

"""
Exercise 2: Fit and interpret linear regression models with Python

Using the merged dataframe from the previous section, you will be exploring the
relationships between different features of the data. The statsmodels package
(more here) is an incredibly useful package for conducting statistical tests
and running regressions. As such, it is especially appropriate for the types of
questions we’re interested in here. For this assignment, we’ll be using the
formula api from statsmodels (more here) to run some regressions between
variables in our dataset. You can load this tool into Python with import
statsmodels.formula.api as smf.

Step 2.1

First, you’re interested in exploring if there’s a relationship between the
number of DNMs and parental age. Use matplotlib to plot the following. All
plots should be clearly labelled and easily interpretable.

    the count of maternal de novo mutations vs. maternal age (upload as
    ex2_a.png in your submission directory) the count of paternal de novo
    mutations vs. paternal age (upload as ex2_b.png in your submission
    directory)
"""

import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
# Effect of Maternal Age on Maternal DNMs

fig, ax = plt.subplots(figsize=(8, 6))

ax.plot(df_full.iloc[:,1], df_full.iloc[:,2], "o", label="data")
ax.set_xlabel("Maternal Age")
ax.set_ylabel("DNM Count")
ax.set_title("Maternal Age vs DNM Count")

plt.savefig('ex2_a.png')
plt.close()

fig1, ax1 = plt.subplots(figsize=(8, 6))

ax1.plot(df_full.iloc[:,0], df_full.iloc[:,3], "o", label="data")
ax1.set_xlabel("Paternal Age")
ax1.set_ylabel("DNM Count")
ax1.set_title("Paternal Age vs DNM Count")

plt.savefig('ex2_b.png')
plt.close()

"""
Step 2.2

Now that you’ve visualized these relationships, you’re curious whether they’re
statistically significant. Perform ordinary least squares using the smf.ols()
function to test for an association between maternal age and maternally
inherited de novo mutations. In your README.md for this assignment, answer the
following questions:

    What is the “size” of this relationship? In your own words, what does this
    mean? Does this match what you observed in your plots in step 2.1? Is this
    relationship significant? How do you know?
"""

m_mod = smf.ols('maternal_dnm ~ Mother_age', data =  df_full)
m_res = m_mod.fit()

#fig, ax = plt.subplots(figsize=(8, 6))
#
#ax.plot(df_full.iloc[:,1], df_full.iloc[:,2], "o", label="data")
#ax.plot(df_full.iloc[:,1], m_res.fittedvalues, "--", label="OLS", color = 'red')
#ax.set_xlabel("Maternal Age")
#ax.set_ylabel("DNM Count")
#ax.set_title("OLS Maternal Age ~ Maternal DNMs")

"""
Step 2.3

As before, perform ordinary least squares using the smf.ols() function, but
this time to test for an association between paternal age and paternally
inherited de novo mutations. In your README.md for this assignment, answer the
following questions:

    What is the “size” of this relationship? In your own words, what does this
    mean? Does this match what you observed in your plots in step 6? Is this
    relationship significant? How do you know?
"""

f_mod = smf.ols('paternal_dnm ~ Father_age', data =  df_full)
f_res = f_mod.fit()


"""
Step 2.4

Using your results from step 2.3, predict the number of paternal DNMs for
a proband with a father who was 50.5 years old at the proband’s time of birth.
Record your answer and your work (i.e. how you got to that answer) in your
README.md.
"""

f_res.predict(pd.DataFrame({'Father_age': [50.5]}))

"""
Step 2.5

Next, you’re curious whether the number of paternally inherited DNMs match the
number of maternally inherited DNMs. Using matplotlib, plot the distribution of
maternal DNMs per proband (as a histogram). In the same panel (i.e. the same
axes) plot the distribution of paternal DNMs per proband. Make sure to make the
histograms semi-transparent so you can see both distributions. Upload as
ex2_c.png in your submission directory.
"""

fig1, ax1 = plt.subplots()

ax1.hist(df_full.iloc[:,2], color = 'pink', alpha = 0.5, label = 'Maternal DNMs')
ax1.hist(df_full.iloc[:,3], color = 'lightblue', alpha = 0.5, label = 'Paternal DNMs')
ax1.set_ylabel('Count')
ax1.set_xlabel('Number of DNMs')
plt.legend()
plt.savefig('ex2_c.png')

"""
Step 2.6

Now that you’ve visualized this relationship, you want to test whether there is
a significant difference between the number of maternally vs. paternally
inherited DNMs per proband. What would be an appropriate statistical test to
test this relationship? Choose a statistical test, and find a Python package
that lets you perform this test. If you’re not sure where to look, the stats
module from scipy (more here) provides tools to perform several different
useful statistical tests. After performing your test, answer the following
answers in your README.md for this assignment:

    What statistical test did you choose? Why? Was your test result
    statistically significant? Interpret your result as it relates to the
    number of paternally and maternally inherited DNMs.
"""

import scipy.stats as stats

diff = stats.ttest_ind(a=df_full.iloc[:,3], b = df_full.iloc[:,2], equal_var=True, alternative = 'greater')
