# machine-learning
<b>0. Interactive grouping </b> OOP example 

Module combiner.py implements the analog of the unit "Interactive grouping" of SAS Miner, including a graphical interface. Git posted a version with reduced functionality, which allows to work only with categorical characteristics and replacement values characteristics labels groups instead of woe. Written for python 3.6.1.

Grouping is used in classification tasks. For categorially signs "grouping" is reduced to the replacement of the group znachenii sign one.

The entire set of objects of the training sample is divided into non-intersecting subsets, the objects of each of the subsets have their own characteristic value. For each subset it is possible to determine the proportion of objects of the target class in this podmnozhestva and the confidence interval for this proportion. Subsets with overlapping confidence intervals are merged. A new, derived, categorical trait is obtained by replacing the values that allocate the merged subsets with a single label.

<b>1. Churn prediction </b>  

Preprocessing, feature selection, model quality dependance on preprocessing
pandas, skipy, sklearn, seaborn. 

<b>2. Credit score </b>

statistical hypothesis testing

<b>3. Time series analysis </b>

forecast of the average salary with SARIMAX

<b>4. Sentiment analysis </b>

tonality analysis with nltk.

<b>5. Simple clustering </b>

PCA + DBSCAN

<b>6. Choice of banner </b>

marketing task solution

<b>7. Fraud on road </b>

find clients with potential fraud

<b>8. Simple client-server </b>

asyncio, python3

<b>9. SQL with python </b>

<b>10. Working with logs </b>

<b>11. NN for Time Series </b>

Application of a fully connected neural network of direct propagation to predict a large number (~6000 thousand) of time series of load on employees of Bank branches. The application of this approach made it possible to achieve a higher quality of the forecast, to reduce the time of training and the application of the model, in comparison with the approach involving the training of SARIMAX with exogenous characteristics for each series separately.
