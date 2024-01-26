import numpy as np
import random as rand
import math
import scipy.stats as stats

""" Create a normal distribution with mean and std """

""" Weight the perturbation angles with a normal distribution """
angles = np.linspace(-math.pi/4, math.pi/4, 100)
""" Create  a normal distribution with mean and std """
weights = stats.norm.pdf(angles, 1 , 0.0001)

for k in range(1000):
    perturbation_lession = rand.choices(angles, weights=weights, k=1)[0]
    
pert_mean = np.mean(perturbation_lession)

print(pert_mean)
