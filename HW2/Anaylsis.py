import numpy as np
import seaborn as sns
import pandas as pd

""" Load the data from the csv file and perform the analysis."""
df = pd.read_csv('error_angles_Flo.csv')

""" Calulate the motor varibility or the std for each baseline and each trial."""
MV = df[df['trial_name'] == 'Basline']['error_angles'].std()
adaptation_rate = np.max(100 * (MV / df[df['trial_name'] != 'Basline']['error_angles'] -1), 0)
trials = df[df['trial_name'] != 'Basline'].trial_name

""" Plot the adaptation rate but not for the baseline."""
g0 = sns.scatterplot(x= trials, y= adaptation_rate, data=df[df['trial_name'] != 'Basline'])
g0 = sns.lineplot(x= trials, y= adaptation_rate, data=df[df['trial_name'] != 'Basline'])

subject = df.subject_name.unique()

g0.figure.savefig("error_angles_"+ subject + ".svg")
