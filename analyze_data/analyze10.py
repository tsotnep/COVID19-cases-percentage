import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import json
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)
import gc

# daily cases by countries, improvement of script analyze5, now this accepts list of countries and generates separate files
#changables>>
countriesOfInterest = ['Georgia']
fromFirstNOfCases = 100
path_popul      ="../parsed_population.json"
path_cases      ="../parsed_cases.json"
path_confr      ="../parsed_casesByDaysConfirmed.json"
path_death      ="../parsed_casesByDaysDeaths.json"
path_recov      ="../parsed_casesByDaysRecovered.json"
#<<changables

if not os.path.exists('../temp'):
    os.makedirs('../temp')

for c in range (0, len(countriesOfInterest)):
    graphImgPath    ="../temp/img10_daily_"+countriesOfInterest[c]+".png"
    popul_json      = json.load(open(path_popul))
    cases_json      = json.load(open(path_cases))
    confr_json      = json.load(open(path_confr))
    death_json      = json.load(open(path_death))
    recov_json      = json.load(open(path_recov))

    popul       = pd.DataFrame.from_dict(popul_json)
    cases       = pd.DataFrame.from_dict(cases_json)
    confr       = pd.DataFrame.from_dict(confr_json,orient='index')
    death       = pd.DataFrame.from_dict(death_json,orient='index')
    recov       = pd.DataFrame.from_dict(recov_json,orient='index')

    #filter data
    popul.drop(popul.loc[popul['country'].eq(countriesOfInterest[c])==False].index, inplace=True) #remove countries out of our interest
    cases.drop(cases.loc[cases['country'].eq(countriesOfInterest[c])==False].index, inplace=True) #remove countries out of our interest
    confr.drop(confr.loc[confr['country'].eq(countriesOfInterest[c])==False].index, inplace=True) #remove countries out of our interest
    death.drop(death.loc[death['country'].eq(countriesOfInterest[c])==False].index, inplace=True) #remove countries out of our interest
    recov.drop(recov.loc[recov['country'].eq(countriesOfInterest[c])==False].index, inplace=True) #remove countries out of our interest

    #reindex
    cases.reset_index(drop=True, inplace=True) #remove old indexes and add new
    popul.reset_index(drop=True, inplace=True) #remove old indexes and add new
    confr.reset_index(drop=True, inplace=True) #remove old indexes and add new
    death.reset_index(drop=True, inplace=True) #remove old indexes and add new
    recov.reset_index(drop=True, inplace=True) #remove old indexes and add new

    firstIndR=1
    totalRecov=0
    for i in range(len(recov.columns)-2, 2,-1): #calculate daily-new-cases from total-day cases
        ind1=str(i)
        ind2=str(i-1)
        if (recov.at[0,ind1]==0 and firstIndR==1): firstIndR=i
        recov.at[0,ind1]=recov.iloc[0][ind1] - recov.iloc[0][ind2]
        totalRecov += recov.at[0,ind1]

    firstIndD=1
    totalDeath=0
    for i in range(len(death.columns)-2, 2,-1): #calculate daily-new-cases from total-day cases
        ind1=str(i)
        ind2=str(i-1)
        if (death.at[0,ind1]==0 and firstIndD==1): firstIndD=i
        death.at[0,ind1]=death.iloc[0][ind1] - death.iloc[0][ind2]
        totalDeath += death.at[0,ind1]

    firstIndC=1
    totalConfr=0
    for i in range(len(confr.columns)-2, 2,-1): #calculate daily-new-cases from total-day cases
        ind1=str(i)
        ind2=str(i-1)
        if (confr.at[0,ind1]>=fromFirstNOfCases): firstIndC=i
        confr.at[0,ind1]=confr.iloc[0][ind1] - confr.iloc[0][ind2]
        totalConfr += confr.at[0,ind1]

    fig, ax = plt.subplots()
    ax.bar(np.arange(firstIndC, confr.iloc[0].count())-0.3,     confr.iloc[0][firstIndC:].values,   width=0.3, align='center', color='blue',  label='Daily New Cases')
    ax.bar(np.arange(firstIndC, recov.iloc[0].count()),         recov.iloc[0][firstIndC:].values,   width=0.3, align='center', color='orange', label='Daily Recoveries')
    ax.bar(np.arange(firstIndC, death.iloc[0].count())+0.3,     death.iloc[0][firstIndC:].values,   width=0.3, align='center', color='black',   label='Daily Deaths')

    ax.set_ylabel('Daily Recoveries-Deaths-Cases')
    ax.set_xlabel('days from first '+str(fromFirstNOfCases)+'cases, till today')
    ax.set_title(countriesOfInterest[c]+', All time Total Cases/Recoveries/Deaths :'+str(int(totalConfr))+'/'+str(int(totalRecov))+'/'+str(int(totalDeath)))
    ax.legend()
    ax.grid(which='major',axis='y')
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    fig.savefig(graphImgPath, dpi = 300)
    gc.collect()
