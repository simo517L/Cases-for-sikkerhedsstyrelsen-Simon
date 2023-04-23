import pandas as pd
import numpy as np
import scipy as sci
from matplotlib import pyplot as plt


new_husrapport = pd.read_csv('new_husrapport.csv') #loaded data

# Laver to ny datasæt ud fra hvilke faggruppe insepktørene er i.
Faggruppe1_rapport =  new_husrapport[new_husrapport['Faggruppe'] == 'Faggruppe1']
# Plotter det, og ser at der en del outliers, hvor vi fjerner nogen af dem
plt.plot(Faggruppe1_rapport['færdiggørelsestiden'],'bs')
Faggruppe1_rapport = Faggruppe1_rapport.drop(Faggruppe1_rapport[Faggruppe1_rapport.færdiggørelsestiden > 10000].index)
plt.plot(Faggruppe1_rapport['færdiggørelsestiden'],'bs')


Faggruppe2_rapport =  new_husrapport[new_husrapport['Faggruppe'] == 'Faggruppe2']
plt.plot(Faggruppe2_rapport['færdiggørelsestiden'],'bs')
Faggruppe2_rapport = Faggruppe2_rapport.drop(Faggruppe2_rapport[Faggruppe2_rapport.færdiggørelsestiden > 10000].index)
plt.plot(Faggruppe2_rapport['færdiggørelsestiden'],'bs')

#Aflæser størelsen af Faggruppe 1, den gennesitlige færdiggørelsestid og den tilhøredne variance
print(len(Faggruppe1_rapport['færdiggørelsestiden']))
print(np.mean(Faggruppe1_rapport['færdiggørelsestiden']))
print(np.var(Faggruppe1_rapport['færdiggørelsestiden']))

#Aflæser størelsen af Faggruppe 2, den gennesitlige færdiggørelsestid og den tilhøredne variance
print(len(Faggruppe2_rapport['færdiggørelsestiden']))
print(np.mean(Faggruppe2_rapport['færdiggørelsestiden']))
print(np.var(Faggruppe2_rapport['færdiggørelsestiden']))

# Laver en t.test for af se om grupperne har samme middelværdi
print(sci.stats.ttest_ind(Faggruppe1_rapport['færdiggørelsestiden'],Faggruppe2_rapport['færdiggørelsestiden'],equal_var=False))



# Laver boxplots over de to gruppe for af se på forskellen på varians
my_dict = {'Faggruppe1': Faggruppe1_rapport['færdiggørelsestiden'], 'Faggruppe2': Faggruppe2_rapport['færdiggørelsestiden']}

fig, ax = plt.subplots()
ax.boxplot(my_dict.values())
ax.set_xticklabels(my_dict.keys())


# Fjerner flere outliers for af gøre plot mere læsbart
Faggruppe1_rapport = Faggruppe1_rapport.drop(Faggruppe1_rapport[Faggruppe1_rapport.færdiggørelsestiden > 5000].index)
Faggruppe2_rapport = Faggruppe2_rapport.drop(Faggruppe2_rapport[Faggruppe2_rapport.færdiggørelsestiden > 5000].index)

my_dict = {'Faggruppe1': Faggruppe1_rapport['færdiggørelsestiden'], 'Faggruppe2': Faggruppe2_rapport['færdiggørelsestiden']}

fig, ax = plt.subplots()
ax.boxplot(my_dict.values())
ax.set_xticklabels(my_dict.keys())

print(sci.stats.ttest_ind(Faggruppe1_rapport['færdiggørelsestiden'],Faggruppe2_rapport['færdiggørelsestiden'],equal_var=False))

