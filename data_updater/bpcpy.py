"""Creates confidence intervals using the beta product confidence procedure 
Calculated using the method of moments
Results with my cricket dataset were verified against results attained using the
R 'bpcp' package for discrete grouped data with censoring
Feed in an event table made by the lifelines package"""

from scipy.stats import beta
import pandas as pd


def confidence_intervals(df, alpha=0.05):
    """uses the method of moments approach to calculate confidence intervals
    following the beta product confidence procedure"""
    
    df['at_risk_next'] = df.at_risk.shift(-1)
    df['at_risk_next'].iloc[-1] = df['at_risk'].iloc[-1] - df['removed'].iloc[-1]
    km, upper_u, upper_t, lower_u, lower_t = 1, 1, 1, 1, 1
    results_dict = {'time': [0] + df.index.tolist(), 'survival': [1], 'lower': [], 'upper': [1]}
    lower = beta.ppf(alpha/2, df.at_risk[1], 1)
    results_dict['lower'].append(lower)

    for n, m, c, s in zip(df.at_risk, df.observed, df.censored, df.at_risk_next):
        y = n - m + 1
        j = m
        upper_u *= y/(y+j)
        upper_t *= y*(y+1)/((y+j)*(y+j+1))

        a = upper_u*(upper_u-upper_t)/(upper_t-upper_u**2)
        b = (1-upper_u)*(upper_u-upper_t)/(upper_t-upper_u**2)
        upper = beta.ppf(1-alpha/2, a, b)
        results_dict['upper'].append(upper)

        if s:
            lower_u = upper_u * s / (s + 1)
            lower_t = upper_t * s * (s + 1) / ((s + 1) * (s + 1 + 1))
            a = lower_u * (lower_u - lower_t) / (lower_t - lower_u ** 2)
            b = (1 - lower_u) * (lower_u - lower_t) / (lower_t - lower_u ** 2)
            lower = beta.ppf(alpha / 2, a, b)
        else:
            lower = 0

        results_dict['lower'].append(lower)
        km *= 1-m/n
        results_dict['survival'].append(km)
    kmwCL = pd.DataFrame(results_dict)
    return kmwCL
