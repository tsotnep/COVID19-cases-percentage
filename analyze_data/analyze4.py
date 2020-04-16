import json
import requests 
import numpy as np
import pandas as pd

import csv
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from itertools import cycle
from itertools import repeat
import copy
import os

#changables>>

countriesOfInterest = ['Croatia','Estonia','Armenia','Lithuania','Bulgaria','Latvia','Georgia'] #comment if you need long list of countries
graphImgPath="../img4_cases"+'-'.join(countriesOfInterest)+".png"
fromFirstNofCases = 1 
Normalized = False #normalized cases by country, meaning divide all day's cases by country's population, make it True if you want so.
path_casesByDays="https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json"
path_population="../parsed_population.json"
showCases = True
showRecoveries = False
showDeaths = False
#<<changables


#leave only the countries we need
population_json = json.load(open(path_population))
population = pd.DataFrame.from_dict(population_json)
population.drop(population.loc[population['country'].isin(countriesOfInterest)==False].index, inplace=True) #remove countries out of our interest
population.reset_index(drop=True, inplace=True) #remove old indexes and add new

#leave only the countries we need
cases_json = requests.get(path_casesByDays).json()
cases = pd.DataFrame(cases_json)
cases = cases[cases.columns.intersection(countriesOfInterest)]

#create dataframe and fill with data
confirmedBydays = pd.DataFrame()
deathsBydays = pd.DataFrame()
recoveredBydays = pd.DataFrame()
firstCases = pd.DataFrame()
for country in countriesOfInterest:
    firstCaseFound=False
    for days in range(cases[cases.columns[0]].count()):
        confirmedBydays.at[country, days] = cases[country][days]['confirmed']
        deathsBydays.at[country, days] = cases[country][days]['deaths']
        recoveredBydays.at[country, days] = cases[country][days]['recovered']
        if (firstCaseFound == False and cases[country][days]['confirmed'] >= fromFirstNofCases): 
            firstCaseFound = True
            firstCases.at[country,0] = days

#TODO: add normalization with population

fig, ax = plt.subplots()
lines = ["-","--","-."] #line types
linecycler = cycle(lines)
for country in countriesOfInterest:
    firstCaseIndex=int(firstCases.loc[country])
    lastCaseX=int(cases[cases.columns[0]].count())-1
    if (showRecoveries): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), recoveredBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' recov')
        lastCaseY=int(recoveredBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY),fontsize=6)
    if (showDeaths): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), deathsBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' death')
        lastCaseY=int(deathsBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY),fontsize=6)
    if (showCases): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), confirmedBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' cases')
        lastCaseY=int(confirmedBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY),fontsize=6)

ax.set(xlabel='days', ylabel='N of cases', title="from first "+str(fromFirstNofCases)+"  cases")
ax.grid()

#legend location
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.05, box.width, box.height])
ax.legend(fontsize=6, loc='upper center', bbox_to_anchor=(0.5, -0.1),fancybox=False, shadow=False, ncol=5)

#save to file
fig.savefig(graphImgPath, dpi = 300)