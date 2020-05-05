# confirmed percentage of total tests
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import json
import numpy as np
path_population="../parsed_population.json"
path_cases="../parsed_cases.json"
graphImgPath="../img2_confirmed_percentage.png"
countriesOfInterest = ['Georgia', 'Armenia', 'Bulgaria', 'Lithuania', 'Croatia', 'Estonia', 'Latvia' ] #comment if you need long list of countries

population_json = json.load(open(path_population))
cases_json      = json.load(open(path_cases))

population = pd.DataFrame.from_dict(population_json)
cases      = pd.DataFrame.from_dict(cases_json)

#filter data
population.drop(population.loc[population['country'].isin(countriesOfInterest)==False].index, inplace=True) #remove countries out of our interest
cases.drop(cases.loc[cases['country'].isin(countriesOfInterest)==False].index, inplace=True) #remove countries out of our interest

#reindex
cases.reset_index(drop=True, inplace=True) #remove old indexes and add new
population.reset_index(drop=True, inplace=True) #remove old indexes and add new

#map populations to countrie
for country in countriesOfInterest:
    cases.at[(cases.loc[cases['country'] == country ].index[0]), 'population'] = population.at[(population.loc[population['country'] == country ].index[0]), 'population']

#calculate what percentage of population is tested
cases['confirmed_tests'] = round(cases['cases']*100/cases['tests'],2)

#graph
plt.rcdefaults()
fig, ax = plt.subplots()
ax.barh(np.arange(cases['country'].count()), cases['confirmed_tests'], align='center')
ax.set_yticks(np.arange(cases['country'].count()))
ax.set_yticklabels(cases['country']+',\n'+cases['cases'].astype(str)+' / '+cases['tests'].astype(str),fontsize=5)
ax.invert_yaxis()
ax.set_xlabel('percentage')
ax.set_title('percentage of confirmed cases from total tests')
fig.savefig(graphImgPath, dpi = 900)