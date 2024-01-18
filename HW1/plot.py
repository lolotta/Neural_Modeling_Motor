import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
a1, a2, a3, a4, a5, a6 = 0, 40, 80, 120, 160, 200
collect_attempts = [a2, a3, a4, a5, a6]
string_attempts = ['No Perturbation', 'Gradual Perturbation', 'No Perturbation', 'Sudden Perturbation', 'Random Perturbation']
subject_name = "Lotta"
attempts = 200
import os
print(os.getcwd())
data = pd.read_csv("HW5/error_angles_"+ subject_name + ".csv")

g0 = sns.scatterplot(data = data, x = 'attempts', y = 'error_angles') 
g0 = sns.lineplot(data = data, x = 'attempts', y = 'error_angles')
""" Add vertical lines to show the different pertubation_types."""
g0.vlines(np.array(collect_attempts) - 0.5, ymin = -45, ymax = 40, color = 'red', alpha = 0.5)
""" Add labels to the vertical lines."""
for i in range(len(collect_attempts)):
    g0.text(collect_attempts[i] - 7, -45, string_attempts[i], rotation = 90, color = 'red', alpha = 0.5)
g0.set(xlabel='attempts', ylabel='error_angles', title = 'Error_angles over attempts')
plt.show()

g0.figure.savefig("HW5/error_angles_"+ subject_name + ".png")
