import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import json
import numpy as np

path_population="../parsed_population.json"
path_cases="../parsed_cases.json"
graphImgPath="../plot.png"
countriesOfInterest = ['Georgia', 'Armenia', 'Bulgaria', 'Lithuania', 'Croatia', 'Estonia', 'Latvia' ] #comment if you need long list of countries

population_json = json.load(open(path_population))
cases_json      = json.load(open(path_cases))

population = pd.DataFrame.from_dict(population_json)
cases      = pd.DataFrame.from_dict(cases_json)

#pd.set_option('display.max_rows', None)

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
cases['tested_Population']   = cases['tests']*100/cases['population']
cases['infected_Population'] = cases['cases']*100/cases['population']
cases['active_Population']   = cases['active']*100/cases['population']

#graph
plt.rcdefaults()
fig, ax = plt.subplots()
x_pos = np.arange(cases['country'].count())
rects1=ax.bar(x_pos+0.2, cases['deaths'],                 label='death cases',                 width=0.2, align='center', color='red')
rects2=ax.bar(x_pos-0.2, cases['recovered'],              label='recovered cases',           width=0.2, align='center', color='green')
rects3=ax.bar(x_pos,     cases['active'],                 label='active cases',          width=0.2, align='center', color='blue')
ax.set_xticks(x_pos)
ax.set_xticklabels(cases['country']+'\n tested \n population in % \n'+round(cases['tested_Population'],5).astype(str),fontsize=5)
ax.set_ylabel('cases')
ax.set_title('cases by country')
ax.legend()

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.01*h, '%d'%int(h),
                ha='center', va='bottom')

autolabel(rects1)
autolabel(rects2)
autolabel(rects3)



fig.savefig(graphImgPath, dpi = 900)