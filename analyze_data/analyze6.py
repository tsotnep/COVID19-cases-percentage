# daily cases by countries
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os
import json
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter,AutoMinorLocator)

#changables>>
countriesOfInterest = ['Azerbaijan', 'Georgia', 'Armenia', 'Turkey', 'Estonia', 'Latvia', 'Lithuania', 'US', 'Germany','Italy','Spain','Greece', 'United Kingdom', 'Russia','China','Portugal','Poland']
path_popul      ="../parsed_population.json"
path_cases      ="../parsed_cases.json"
path_confr      ="../parsed_casesByDaysConfirmed.json"
path_death      ="../parsed_casesByDaysDeaths.json"
path_recov      ="../parsed_casesByDaysRecovered.json"
#<<changables

if not os.path.exists('../temp/an6'):
    os.makedirs('../temp/an6')

for c in range (0, len(countriesOfInterest)):
    graphImgPath    ="../temp/an6/cases_"+countriesOfInterest[c]+".png"
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

    firstInd=1
    totalConfr=0
    for i in range(len(confr.columns)-2, 2,-1): #calculate daily-new-cases from total-day cases
        ind1=str(i)
        ind2=str(i-1)
        if (confr.at[0,ind1]==0 and firstInd==1): firstInd=i
        confr.at[0,ind1]=confr.iloc[0][ind1] - confr.iloc[0][ind2]
        totalConfr += confr.at[0,ind1]


    fig, ax = plt.subplots()
    ax.bar(np.arange(confr.iloc[0].count()-firstInd), confr.iloc[0][firstInd:].values, align='center')
    ax.set_ylabel('cases')
    ax.set_xlabel('days from first case')
    ax.set_title(countriesOfInterest[c]+', new cases by days. Total confirmed cases : '+str(totalConfr))
    ax.grid(which='major')
    ax.xaxis.set_minor_locator(MultipleLocator(5))
    fig.savefig(graphImgPath, dpi = 300)


