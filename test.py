import pandas as pd
teamdf = pd.read_csv('teams.csv')
dict = {}
dict['TEST1'] = 2
dict['TEST2'] = 2
dict['TEST3'] = 10
fdict = {}
for x in dict.keys():
    fdict[x.title()] = dict[x]
for i in range(2):
    print(i)