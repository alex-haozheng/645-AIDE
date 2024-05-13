# prunign and sharing based optimization
from math import log, pi

# n is len(v1)
# 
def calc_running_confidence_interval(m, n, d):
	x = (1-(m-1)/n)*2*log(log(m))+log(pi**2/3*d)
	return (x/(2*m))**0.5


# split dataset #every split call calc_running ... 

# every tuple amf kl-divergence (utility fx) 
# some tuple amf (if low) get rid of it 

# some tuple amf-amf_1