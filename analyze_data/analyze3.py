import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import json
import numpy as np
# tested percentage of population
path_population="../parsed_population.json"
path_cases="../parsed_cases.json"
graphImgPath="../img3_tested_Percentage.png"
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
cases['tests_pop'] = cases['tests']*100/cases['population']
cases['cases_pop'] = cases['cases']*100/cases['population']
cases['activ_pop'] = cases['active']*100/cases['population']
cases['death_pop'] = cases['deaths']*100/cases['population']
cases['recov_pop'] = cases['recovered']*100/cases['population']

#graph
plt.rcdefaults()
fig, ax = plt.subplots()
x_pos = np.arange(cases['country'].count())
rects1=ax.bar(x_pos-0.4, cases['tests_pop'],                        width=0.2, align='center', color='yellow'     , label='tested population in %')
rects2=ax.bar(x_pos-0.2, cases['cases_pop'],                        width=0.2, align='center', color='orange'   , label='total cases of population in %')
ax.set_xticks(x_pos)
ax.set_xticklabels(cases['country']+'\n tests: '+round(cases['tests'],5).astype(str)+'\n population: '+(round(cases['population']/1000000,2).astype(str)),fontsize=5)
ax.set_ylabel('percentage')
ax.set_title('cases by country')
ax.legend()

#ax.set(ylim=(0, 0.1))

def autolabel(rects):
    for rect in rects:
        h = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 0.01*h, '%f'%float(h),
                ha='center', va='bottom',rotation=90, fontsize=7)

autolabel(rects1)
autolabel(rects2)


fig.savefig(graphImgPath, dpi = 900)