import pandas as pd
import numpy as np
import scipy as sci

from matplotlib import pyplot as plt
import os
husrapport = pd.read_csv('husrapporter-2021-01.csv') #loaded data



# finde de ejendome som fremkommmer i datasætter mere eller mindre end 2 gange
ejendome = husrapport['ejendoms_id']

uniqe_ejendome, count_ejendome= np.unique(ejendome,return_counts=True)

ejendome_nodup = uniqe_ejendome[count_ejendome == 2]

new_husrapport = husrapport.loc[husrapport['ejendoms_id'].isin(ejendome_nodup)]

# Fjerne fjelrapportering da datoen ikke giver mening
new_husrapport = new_husrapport.drop(8477) # husk af fjerne det andet hus

#print(len(new_husrapport))
new_husrapport = new_husrapport[new_husrapport['gyldighedsdato'] != '1-01-01 12:00:00']
new_husrapport = new_husrapport[new_husrapport['oprettelsesdato'] != '1-01-01 12:00:00']
new_husrapport = new_husrapport[new_husrapport['besoegsdato'] != '1-01-01 12:00:00']
# omdanner de tre tidsvariable til datetime data typer, så vi kan arbejde med dem
new_husrapport['gyldighedsdato'] = pd.to_datetime(new_husrapport['gyldighedsdato'])
new_husrapport['oprettelsesdato'] = pd.to_datetime(new_husrapport['oprettelsesdato'])
new_husrapport['besoegsdato'] = pd.to_datetime(new_husrapport['besoegsdato'])


# Fjerne alle de rækker hvor gyldighedsdatoen ligger før besoegsdato
new_husrapport = new_husrapport.loc[new_husrapport['gyldighedsdato'] > new_husrapport['besoegsdato']]


Faggruppe1 = []
Faggruppe2 = []

# Vi vælger først den inspektør som har arbejder på flest ejendome og tilføre inspektøren til gruppe 1
first_inspektoer = new_husrapport['inspektoer_id'].value_counts().idxmax()
Faggruppe1.append(first_inspektoer)

# Så finde vi de ejendome som inspektøren har arbejdet på og tilføre så de inspektører som har arbejde på samme ejendom til gruppe 2
ejendome_check = new_husrapport[new_husrapport['inspektoer_id'] == first_inspektoer]['ejendoms_id']
new_husrapport_temp = new_husrapport.loc[new_husrapport['ejendoms_id'].isin(ejendome_check)]
To_fag2 = new_husrapport_temp[new_husrapport_temp['inspektoer_id'] != first_inspektoer]["inspektoer_id"]
To_fag2 = To_fag2.unique()
To_fag2 = To_fag2.tolist()
Faggruppe2 = Faggruppe2 + To_fag2

# Vi laver nogle lister over hvilke ejendomme vi har tjekket
ejendome_checked1 = []
ejendome_checked2 = ejendome_check
ejendome_checked2 = ejendome_checked2.to_list()
# Køre et while loop indtil vi har tjekket alle ejendomme igennem for begge grupper
while  len(ejendome_checked1) != len(ejendome_checked2):
    #print(len(ejendome_checked2))
    ejendome_checked1 = ejendome_checked2
    ejendome_check = new_husrapport[new_husrapport['inspektoer_id'].isin(To_fag2)]['ejendoms_id']
    ejendome_check = ejendome_check[~ejendome_check.isin(ejendome_checked2)]
    new_husrapport_temp = new_husrapport.loc[new_husrapport['ejendoms_id'].isin(ejendome_check)]
    To_fag1 = new_husrapport_temp[~new_husrapport_temp['inspektoer_id'].isin(To_fag2)]["inspektoer_id"]
    To_fag1 = To_fag1.unique()
    To_fag1 = To_fag1.tolist()
    Faggruppe1 = Faggruppe1 + To_fag1

    ejendome_checked2 =ejendome_checked2 + ejendome_check.to_list()

    ejendome_check = new_husrapport[new_husrapport['inspektoer_id'].isin(To_fag1)]['ejendoms_id']
    ejendome_check = ejendome_check[~ejendome_check.isin(ejendome_checked2)]
    new_husrapport_temp = new_husrapport.loc[new_husrapport['ejendoms_id'].isin(ejendome_check)]
    To_fag2 = new_husrapport_temp[~new_husrapport_temp['inspektoer_id'].isin(To_fag1)]["inspektoer_id"]
    To_fag2 = To_fag2.unique()
    To_fag2 = To_fag2.tolist()
    Faggruppe2 = Faggruppe2 + To_fag2

    ejendome_checked2 =ejendome_checked2 + ejendome_check.to_list()


#print(len(ejendome_checked2))
#print(len(Faggruppe1))
#print(len(Faggruppe2))
#print(len(Faggruppe2))

# Laver en ny version af datasættet, hvor vi kun beholder de inspektoer som er i en af de to grupper
new_husrapport = new_husrapport.loc[new_husrapport['inspektoer_id'].isin(Faggruppe1+Faggruppe2)]

# Laver en ny søjle i datasættet hvor der står hvilke faggruppe en inspektoer er i
new_husrapport['Faggruppe'] =np.where(new_husrapport['inspektoer_id'].isin(Faggruppe1),'Faggruppe1','Faggruppe2')

# Laver en søjle for færdiggørelsestiden, som omdannes til minutter
new_husrapport['færdiggørelsestiden'] = (new_husrapport['gyldighedsdato']-new_husrapport['besoegsdato']).fillna(0)
new_husrapport['færdiggørelsestiden'] = new_husrapport['færdiggørelsestiden'].dt.total_seconds()/60

new_husrapport.to_csv(os.getcwd()+'\\new_husrapport.csv', index=False) # gemmer datasættet


