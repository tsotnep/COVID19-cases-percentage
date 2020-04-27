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
countriesOfInterest = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic', 'Chad', 'Chile', 'China', 'Colombia', 'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', 'Croatia', 'Diamond Princess', 'Cuba', 'Cyprus', 'Czechia', 'Denmark', 'Djibouti', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 'Guatemala', 'Guinea', 'Guyana', 'Haiti', 'Holy See', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan', 'Kenya', 'Korea, South', 'Kuwait', 'Kyrgyzstan', 'Latvia', 'Lebanon', 'Liberia', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Madagascar', 'Malaysia', 'Maldives', 'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco', 'Namibia', 'Nepal', 'Netherlands', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'San Marino', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Singapore', 'Slovakia', 'Slovenia', 'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Taiwan*', 'Tanzania', 'Thailand', 'Togo', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'Uruguay', 'US', 'Uzbekistan', 'Venezuela', 'Vietnam', 'Zambia', 'Zimbabwe', 'Dominica', 'Grenada', 'Mozambique', 'Syria', 'Timor-Leste', 'Belize', 'Laos', 'Libya', 'West Bank and Gaza', 'Guinea-Bissau', 'Mali', 'Saint Kitts and Nevis', 'Kosovo', 'Burma', 'MS Zaandam', 'Botswana', 'Burundi', 'Sierra Leone', 'Malawi', 'South Sudan', 'Western Sahara', 'Sao Tome and Principe', 'Yemen' ]
path_exportDataframeConfirmed = '../../parsed_casesByDaysConfirmed.json'
path_exportDataframeDeaths    = '../../parsed_casesByDaysDeaths.json'
path_exportDataframeRecovered = '../../parsed_casesByDaysRecovered.json'
path_casesByDays="https://raw.githubusercontent.com/pomber/covid19/master/docs/timeseries.json"
#<<changables

#leave only the countries we need
cases_json = requests.get(path_casesByDays).json()
cases = pd.DataFrame(cases_json)

with open('./countries.txt', 'w') as f:
    f.write("[")
    for item in cases.columns:
        f.write("\'%s\', " % item)
    f.write("]")

cases = cases[cases.columns.intersection(countriesOfInterest)]



#create dataframe and fill with data
confirmedBydays = pd.DataFrame()
deathsBydays = pd.DataFrame()
recoveredBydays = pd.DataFrame()
firstCases = pd.DataFrame()
for country in countriesOfInterest:
    for days in range(cases[cases.columns[0]].count()):
        confirmedBydays.at[country, days] = cases[country][days]['confirmed']
        deathsBydays.at[country, days] = cases[country][days]['deaths']
        recoveredBydays.at[country, days] = cases[country][days]['recovered']

confirmedBydays.reset_index(inplace=True)
confirmedBydays.rename(columns={"index": "country"},inplace=True)
confirmedBydays.to_json(path_exportDataframeConfirmed,orient='index', indent=4)


deathsBydays.reset_index(inplace=True)
deathsBydays.rename(columns={"index": "country"},inplace=True)
deathsBydays.to_json(path_exportDataframeDeaths,orient='index', indent=4)


recoveredBydays.reset_index(inplace=True)
recoveredBydays.rename(columns={"index": "country"},inplace=True)
recoveredBydays.to_json(path_exportDataframeRecovered,orient='index', indent=4)




