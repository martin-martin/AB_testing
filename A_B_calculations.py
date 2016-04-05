
# coding: utf-8

# # Sanity Checks
# https://www.udacity.com/course/viewer#!/c-ud257-nd/l-4156348935/e-4183118947/m-4170338842

# calculating the standard deviation:
# 
# SD = sqrt(p(A) * p(B) / N(A) + N (B))

# In[10]:

def sanity_check(control, experiment):
    '''Checks whether the values are within the confidence interval of a 95% CL.
    
    takes as input the values for both the control and the experiment group.
    calculates the confidence interval at a 95% confidence level.
    calls within_confidence_interval() to check whether the p(est) pass.
    prints a human-readable string informing of the outcome.
    returns True if both values pass, and False if either doesn't.
    '''
    # import math, because useful!
    import math
    # convert the input to floating points, in case they are integers
    control = float(control)
    experiment = float(experiment)
    # we assume random assignment, therefore
    p_control = 0.5
    p_experiment = 0.5
    # calculating the standard deviation
    std = math.sqrt(p_control * p_experiment / (control + experiment))
    
    # assuming a Confidence Level of 95% gives a z-score of 1.96
    # calculating the margin of error
    m = std * 1.96
    
    # creating the confidence interval
    lower_bound = 0.5 - m
    upper_bound = 0.5 + m
    
    # calculating p^ (estimated probability) of control and experiment
    p_est_control = control / (control + experiment)
    p_est_experiment = experiment / (control + experiment)
    
    # checking whether the p values are within the confidence interval
    if within_confidence_interval(p_est_control, lower_bound, upper_bound) and within_confidence_interval(p_est_experiment, lower_bound, upper_bound):
        print "Sanity check passed"
        print "p^(control) =", round(p_est_control, 4), "and", "p^(experiment) =", round(p_est_experiment, 4)
        print "Confidence Interval:", round(lower_bound, 4), '|', '0.5', '|', round(upper_bound, 4)
        return True
    else:
        if not within_confidence_interval(p_est_control, lower_bound, upper_bound):
            print "The control group value of p^= {0} is out of bounds".format(round(p_est_control, 4))
            print "Confidence Interval:", round(lower_bound, 4), '|', '0.5', '|', round(upper_bound, 4)
            return False
        elif not within_confidence_interval(p_est_experiment, lower_bound, upper_bound):
            print "The experiment group value of p^= {0} is out of bounds".format(round(p_est_experiment, 4))
            print "Confidence Interval:", round(lower_bound, 4), '|', '0.5', '|', round(upper_bound, 4)
            return False
    
    
def within_confidence_interval(p_est, lower_bound, upper_bound):
    '''Checks whether a value is within a confidence interval.
    
    takes as input an estimated probability, a lower and an upper bound
    returns True if the value is within and False otherwise.'''
    if (p_est > lower_bound) and (p_est < upper_bound):
        return True
    else:
        return False


# In[12]:

# testing my functions on the course example
sanity_check(64454, 61818)


# In[13]:

# testing on the second course example

events_control = 15348
evetns_experiment = 15312

sanity_check(events_control, evetns_experiment)


# In[18]:

num_cookies_control = 345543
num_cookies_experiment = 344660

sanity_check(num_cookies_control, num_cookies_experiment)


# In[14]:

clicks_control = 28378
clicks_experiment = 28325

sanity_check(clicks_control, clicks_experiment)


# # Effect Size

# In[34]:

N_rows = 23

ex_clicks = 17260.0
ex_enrolls = 3423.0
ex_pays = 1945.0

cont_clicks = 17293.0
cont_enrolls = 3785.0
cont_pays = 2033.0

# gross conversion = enrolls/clicks
# net conversion = pays/clicks

def effect_size(n_control, x_control, n_experiment, x_experiment, d_min):
    import math
    # converting to float to account for integer input
    n_control, x_control = float(n_control), float(x_control)
    n_experiment, x_experiment = float(n_experiment), float(x_experiment)
    # calculating pooled probability
    p_pooled = (x_control + x_experiment) / (n_control + n_experiment)
    # calculating pooled standard error
    se_pooled = math.sqrt(p_pooled * (1 - p_pooled) * (1 / n_control + 1 / n_experiment))
    # estimated difference
    d_hat = (x_experiment / n_experiment) - (x_control / n_control)
    # margin of error @ 95% CL (z-score = 1.96)
    z_score = 1.96
    m = se_pooled * z_score
    # CI (lower and upper bound)
    lower_bound = d_hat - m
    upper_bound = d_hat + m
    # printing the CI in decimal number format
    print "CI: {0} | {1} | {2}".format('%f' % lower_bound, '%f' % d_hat, '%f' % upper_bound)
    # deciding on statistical and practical significance
    if d_min < lower_bound or dmin > upper_bound:
        print "practical significance boundary is NOT within the CI"
    return d_min
    

# calculating effect size for gross conversion (dmin= 0.01)
d_min_gross_conversion = 0.01
print "Gross Conversion", effect_size(cont_clicks, cont_enrolls, ex_clicks, ex_enrolls, d_min_gross_conversion)

# calculating effect size for net conversion (dmin= 0.0075)
d_min_net_conversion = 0.0075
print "Net Conversion", effect_size(cont_clicks, cont_pays, ex_clicks, ex_pays, d_min_net_conversion)

