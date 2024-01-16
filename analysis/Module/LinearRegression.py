## Linear regression
import numpy as np
from scipy.stats import linregress
def get_regression(time, stress):
    slope, intercept, r_value, p_value, std_err = linregress(np.log10(time), np.log10(stress))
    trange = np.round([min(time)-min(time)/10, max(time)+max(time)/10], 0)
    srange = np.round([min(stress)-min(stress)/10, max(stress)+max(stress)/10], 0)
    time_reg = np.arange(trange[0], trange[1], 0.1)
    stress_reg = 10**(slope * np.log10(time_reg) + intercept)
    #limit = 1.96 * std_err/np.sqrt(len(time)) ## 95% sigma2
    time9 = np.round( 10**((np.log10(9) - intercept)/slope), 1)
    return time9, time_reg, stress_reg, trange, srange, r_value, p_value, std_err
