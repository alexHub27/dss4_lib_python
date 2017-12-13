import numpy as np

from statsmodels.tsa.stattools import adfuller,lagmat, lagmat2ds, add_trend
from statsmodels.tsa.adfvalues import mackinnonp, mackinnoncrit
from statsmodels.tools.tools import add_constant, Bunch

from statsmodels.regression.linear_model import OLS, yule_walker


def coint_alex(y0, y1, trend='c', maxlag=None, autolag='aic'):
    """Test for no-cointegration of a univariate equation

    The null hypothesis is no cointegration. Variables in y0 and y1 are
    assumed to be integrated of order 1, I(1).

    This uses the augmented Engle-Granger two-step cointegration test.
    Constant or trend is included in 1st stage regression, i.e. in
    cointegrating equation.

    Parameters
    ----------
    y1 : array_like, 1d
        first element in cointegrating vector
    y2 : array_like
        remaining elements in cointegrating vector
    trend : str {'c', 'ct'}
        trend term included in regression for cointegrating equation
        * 'c' : constant
        * 'ct' : constant and linear trend
        * also available quadratic trend 'ctt', and no constant 'nc'

    method : string
        currently only 'aeg' for augmented Engle-Granger test is available.
        default might change.
    maxlag : None or int
        keyword for `adfuller`, largest or given number of lags
    autolag : string
        keyword for `adfuller`, lag selection criterion.
    return_results : bool
        for future compatibility, currently only tuple available.
        If True, then a results instance is returned. Otherwise, a tuple
        with the test outcome is returned.
        Set `return_results=False` to avoid future changes in return.


    Returns
    -------
    coint_t : float
        t-statistic of unit-root test on residuals
    pvalue : float
        MacKinnon's approximate, asymptotic p-value based on MacKinnon (1994)
    crit_value : dict
        Critical values for the test statistic at the 1 %, 5 %, and 10 %
        levels based on regression curve. This depends on the number of
        observations.

    Notes
    -----
    The Null hypothesis is that there is no cointegration, the alternative
    hypothesis is that there is cointegrating relationship. If the pvalue is
    small, below a critical size, then we can reject the hypothesis that there
    is no cointegrating relationship.

    P-values and critical values are obtained through regression surface
    approximation from MacKinnon 1994 and 2010.

    TODO: We could handle gaps in data by dropping rows with nans in the
    auxiliary regressions. Not implemented yet, currently assumes no nans
    and no gaps in time series.

    References
    ----------
    MacKinnon, J.G. 1994  "Approximate Asymptotic Distribution Functions for
        Unit-Root and Cointegration Tests." Journal of Business & Economics
        Statistics, 12.2, 167-76.
    MacKinnon, J.G. 2010.  "Critical Values for Cointegration Tests."
        Queen's University, Dept of Economics Working Papers 1227.
        http://ideas.repec.org/p/qed/wpaper/1227.html
    """

    trend = trend.lower()
    if trend not in ['c', 'nc', 'ct', 'ctt']:
        raise ValueError("trend option %s not understood" % trend)
    y0 = np.asarray(y0)
    y1 = np.asarray(y1)
    if y1.ndim < 2:
        y1 = y1[:, None]
    nobs, k_vars = y1.shape
    k_vars += 1   # add 1 for y0

    if trend == 'nc':
        xx = y1
    else:
        #xx = add_trend(y1, trend=trend, prepend=False)
        xx = 

    res_co = OLS(y0, xx).fit()

    if res_co.rsquared < 1 - np.sqrt(np.finfo(np.double).eps):
        res_adf = adfuller(res_co.resid, maxlag=maxlag, autolag=None,
                           regression='nc')
    else:
        import warnings
        warnings.warn("y0 and y1 are perfectly colinear.  Cointegration test "
                      "is not reliable in this case.")
        # Edge case where series are too similar
        res_adf = (0,)

    # no constant or trend, see egranger in Stata and MacKinnon
    #if trend == 'nc':
    #    crit = [np.nan] * 3  # 2010 critical values not available
    #else:
    #    crit = mackinnoncrit(N=k_vars, regression=trend, nobs=nobs-1) #N=1 in adfuller
        #  nobs - 1, the -1 is to match egranger in Stata, I don't know why.
        #  TODO: check nobs or df = nobs - k

    pval_asy = mackinnonp(res_adf[0], regression=trend, N=k_vars)
#    if pval_asy<0.01:
    return res_adf[0],pval_asy, res_co.params