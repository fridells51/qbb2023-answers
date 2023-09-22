2.2.1 What is the “size” of this relationship? In your own words, what does this mean? Does this match what you observed in your plots in step 2.1?

The "size" of this relationship is the magnitude of the coefficient, in this case 0.3776.
I interpret this as meaning that for each unit increase in age, the number of predicted probands increases by 0.377566.
This does match the plot in 2.1. The plot in 2.1 shows a clear increase in DNMs as age increases, but the
effect is rather flat. It visually displays a linear relationship between DNMs and age.

2.2.2 Is this relationship significant? How do you know?

I can call `m_res.summary()` and view the summary table and see that the coefficient for maternal age
has a p-value of 0.000 meaning that it is a significant predictor of DNMs in our OLS model.

2.3.1 What is the “size” of this relationship? In your own words, what does this mean? Does this match what you observed in your plots in step 6?

The "size" of this relationship is the magnitude of the coefficient, in this case 1.3538.
I interpret this as meaning that for each unit increase in age, the number of predicted probands increases by 1.3538.
This does match the plot in 2.1. The plot in 2.1 shows a clear increase in DNMs as age increases.
In fathers, the grouping is tight and the relationship is more steep than in mothers.
It visually displays a linear relationship between DNMs and age.


2.3.2 Is this relationship significant? How do you know?

I can call `f_res.summary()` and view the summary table and see that the coefficient for paternal age
has a p-value of 0.000 meaning that it is a significant predictor of DNMs in our OLS model.

2.4.1 Prediction for 50.5 year old father

Ok!

`f_res.predict(pd.DataFrame({'Father_age': [50.5]}))`

This gives me the result: 78.695457 DNMs.

2.6.1 What statistical test did you choose? Why?

I chose the Two-Sample t-Test because that is the correct test to use when comparing the difference between 2 paired samples of
independent data that we can assume are both normally distributed. ANOVA uses an F statistic, which is a squared t statistic so it
really doesn't matter which one I use!

For this case, I assumed equal variances between samples and conducted a one-sided t-Test to determine if the mean of the distribution
underlying paternal DNMs is greater than the mean of the distribution underlying maternal DNMs.

2.6.2 Was your test result statistically significant? Interpret your result as it relates to the number of paternally and maternally inherited DNMs.

Yes! My test was statistically significant. I got a p-value of 0.00.

There is no detectable chance that we would observe results as or more extreme than this due to pure chance given that
the means of the distributions underlying paternal and maternal DNMs are equivalent.
