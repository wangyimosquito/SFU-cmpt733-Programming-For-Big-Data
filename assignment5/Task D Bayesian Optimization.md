# Task D Bayesian Optimization

Hi Niki,



Hope this letter finds you well. 



I know you are working on a project about anomaly detection, and you came to the hyperparameter tunning stage. I am writing this letter to briefly introduce the hyperparameter tuning method you can use in your k-means model for the anomaly detection task. I recommend Bayesian optimization in this case.



Say the hyperparameters are $x$, and the performance of the model using these hyperparameters is $f(x)$, which is the objective function here. Now you want to find $x$ that can maximize $f(x)$. Notice that you don't need to know the exact function of $f$, you only need to know the value of $f(x)$, I use $f(x)$ here only for explanation. Bayesian optimization does this by sampling and points from $f(x)$, and calculating an approximate function that is similar to $f(x)$. In other words, Bayesian optimization has a prior belief about $f(x)$, and keeps updating this prior by sampling. This approximate function is also called the surrogate model. The more sampling, the better we approximate the function. Bayesian optimization also uses an acquisition function to choose samples, it balances between the current best observation and improvements in the surrogate model. To be more specific, if we sample the new point where the surrogate model gives a high objective because it is the most likely objective we want to find but this would not improve the surrogate model. Or we sample somewhere we lack knowledge about, i.e the model prediction uncertainty is high so that the surrogate model could be improved. Both correspond to high acquisition function values and the goal is to maximize the acquisition function to determine the next sampling point. You need to repeat the sampling and updating of the surrogate model until you find a desirable outcome. 



You may wonder why we need to use Bayesian optimization while there are already grid search and randomization strategies. The answer is, sometimes the calculation of the objective function is expensive, and we want to lower the times we search. While grid search basically brute-forces all the possibilities, and random search lacks the information to perform the next try, Bayesian optimization could calculate less while marching toward the right direction. But there are also some drawbacks of Bayesian optimization, for example, it could be stuck at the local optimum and it might perform badly when there are more than 20 hyperparameters.



Should you have any further questions please feel free to contact me.



Best, 

Yiwen Wang