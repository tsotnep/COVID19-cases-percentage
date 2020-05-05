# daily total cases-deaths-recoveries of a country/countries
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

#changables>>
countriesOfInterest = ['Azerbaijan','Georgia','Estonia','US','Italy','Bulgaria','Armenia','Germany']
showCases = True #make it always True
showRecoveries = True #make it True if only single country is in countriesOfInterest
showDeaths = True #make it True if only single country is in countriesOfInterest
graphImgPath="../temp/an9/img9_cases_R_" #country name is concatenated later
fromFirstNOfCases = 100
firstNOfdays = -1
path_casesByDays="https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json"
path_population="../parsed_population.json"
#<<changables


if not os.path.exists('../temp/an9'):
    os.makedirs('../temp/an9')

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

#print (confirmedBydays)
lines = ["-","--","-."] #line types
linecycler = cycle(lines)

for country in countriesOfInterest:
    fig, ax = plt.subplots()
    firstCaseIndex=int(firstCases.loc[country])
    if (showRecoveries): 
        ax.plot(range(firstCaseIndex, cases[cases.columns[0]].count()), recoveredBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' total recoveries') 
    if (showDeaths): 
        ax.plot(range(firstCaseIndex, cases[cases.columns[0]].count()), deathsBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' total deaths')
    if (showCases): 
        ax.plot(range(firstCaseIndex, cases[cases.columns[0]].count()), confirmedBydays.loc[country][firstCaseIndex:], next(linecycler), linewidth=1.5, label=country+' total cases')

    ax.set(xlabel='days', ylabel='N of cases', title="from first "+str(fromFirstNOfCases)+"  cases")
    ax.grid()
    if (firstNOfdays>0):
        plt.xlim(0,firstNOfdays)

    #legend location
    ax.legend()

    graphImagePathByCountry = graphImgPath + country + '.png'
    #save to file
    fig.savefig(graphImagePathByCountry, dpi = 300)