# PHSX815_Week10

This week demonstrates the Central Limit Theorem by showing that the numerically estimated shape parameter of an exponential distribution is distributed according to a normal distribution. 

**Exponential Distribution**

$P(x | \beta) = \frac{1}{\beta} e^{- \frac{x}{\beta}}$,

where $\beta$ is the shape parameter of the distribution, which is the inverse of the rate parameter $\lambda$.

The likelihood is given Bayes' Theorem,

$P(\beta | x) \approx \prod_{i=1}^{N_{meas}} P(x | \beta) = \prod_{i=1}^{N_{meas}} \frac{1}{\beta} e^{- \frac{x_{i}}{\beta}}$.

The log likelihood is more useful and lets us get rid of the exponentials,

$ln(P(\beta | x)) \approx N_{meas} ln(\frac{1}{\beta}) - \frac{1}{\beta} \sum_{i=1}^{N_{meas}} x_{i}$.

Differentiating with respect to $\frac{1}{\beta}$ allows us to maximize the log likelihood and find,

$\beta = \frac{1}{N_{meas}} \sum_{i=1}^{N_{meas}} x_{i}$,

showing that $\beta$ is the mean of the distribution.

![ExponentialPlot.png](https://github.com/DJDdawg/PHSX815_Week10/blob/main/ExponentialPlot.png)
