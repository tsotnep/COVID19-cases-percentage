# compare countries by daily total cases - Raw Data - pick countries with similar size of population
import json
import requests 
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from itertools import cycle
from itertools import repeat
import os
# number of cases normalized/raw by population
#changables>>
countriesOfInterest = ['Azerbaijan','Georgia','Estonia','Bulgaria','Armenia', 'Latvia', 'Lithuania']
#countriesOfInterest = ['Russia'] #Single
Normalized = False # if True, cases/(population in million) 
showCases = True #make it always True
showRecoveries = False #make it True if only single country is in countriesOfInterest
showDeaths = False #make it True if only single country is in countriesOfInterest
graphImgPath="../img5_cases_R_"+'-'.join(countriesOfInterest)+".png"
fromFirstNOfCases = 100
firstNOfdays = -1
path_casesByDays="https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json"
path_population="../parsed_population.json"
#<<changables


#leave only the countries we need
population_json = json.load(open(path_population))
population = pd.DataFrame.from_dict(population_json)
population.drop(population.loc[population['country'].isin(countriesOfInterest)==False].index, inplace=True) #remove countries out of our interest
population.set_index('country',inplace=True, drop=True) #set 'country' to be indexes
population['inMillions'] = round(population['population']/1000000,2)

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
        if (firstCaseFound == False and cases[country][days]['confirmed'] >= fromFirstNOfCases): 
            firstCaseFound = True
            firstCases.at[country,0] = days

if (Normalized): 
    for country in countriesOfInterest:
        confirmedBydays.loc[country] = (confirmedBydays.loc[country] / population.at[country,'inMillions'])
        deathsBydays.loc[country] = (deathsBydays.loc[country] / population.at[country,'inMillions'])
        recoveredBydays.loc[country] = (recoveredBydays.loc[country] / population.at[country,'inMillions'])

#print (confirmedBydays)
fig, ax = plt.subplots()
lines = ["-","--","-."] #line types
linecycler = cycle(lines)
for country in countriesOfInterest:
    firstCaseIndex=int(firstCases.loc[country])
    lastCaseX=int(cases[cases.columns[0]].count())-1
    if (showRecoveries): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), recoveredBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' recov') 
        lastCaseY=int(recoveredBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY),fontsize=7)
    if (showDeaths): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), deathsBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' death')
        lastCaseY=int(deathsBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY),fontsize=7)
    if (showCases): 
        ax.plot(range(0, cases[cases.columns[0]].count()-firstCaseIndex), confirmedBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+', '+str(population.at[country,'inMillions'])+'m')
        lastCaseY=int(confirmedBydays.loc[country][lastCaseX])
        ax.text(lastCaseX-firstCaseIndex,lastCaseY,str(lastCaseY)+' '+country,fontsize=5)

if (Normalized):    ax.set(xlabel='days', ylabel='N of cases divided by population in millions', title="from first "+str(fromFirstNOfCases)+" cases, Normalized by population")
else:               ax.set(xlabel='days', ylabel='N of cases', title="from first "+str(fromFirstNOfCases)+"  cases")
ax.grid()
if (firstNOfdays>0):
    plt.xlim(0,firstNOfdays)

#legend location
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.05, box.width, box.height])
ax.legend(fontsize=6, loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=False, shadow=False, ncol=5)

#save to file
if(Normalized): 
    s=list(graphImgPath)
    s[14]="N"
    graphImgPath = "".join(s)
fig.savefig(graphImgPath, dpi = 300)