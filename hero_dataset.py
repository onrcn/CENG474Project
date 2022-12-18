#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import requests
import sys

url ='https://www.dotabuff.com/heroes'
user_agent = {'User-agent': 'Mozilla/5.0'} # we should change our user-agent
response = requests.get(url, headers=user_agent)
html = response.content
soup = BeautifulSoup(html, "lxml")
hero_grid = soup.find_all("div", class_="hero")
heroes = []
heroes.append('Result')
for hero in hero_grid:
    heroes.append(hero.get_text(strip=True))
df = pd.DataFrame(columns=heroes)

class Match:
    def __init__(self, result, radiant, dire, duration):
        self.Result = result
        self.Radiant = radiant
        self.Dire = dire
        self.Duration = duration

    def getResult(self):
        return self.Result
    def getRadiant(self):
        return self.Radiant
    def getDire(self):
        return self.Dire
    def getDuration(self):
        return self.Duration

    def print_attributes(self):
        print(f"Result: {self.Result}")
        print(f"Radiant: {self.Radiant}")
        print(f"Dire: {self.Dire}")
        print(f"Duration: {self.Duration}")

hero_match_url = sys.argv[1]
response = requests.get(hero_match_url, headers=user_agent)
html = response.content
soup = BeautifulSoup(html, 'lxml')
tbody = soup.find_all('tbody')[0]

import re
matches = []

for i in tbody.find_all('tr'):
    victory_data = i.find_all('td')[2].get_text(strip=True)
    winner = re.search(r"^\w+", victory_data) # we are getting the winner data
    result = -1

    if (winner.group() == 'Radiant'):
        result = 0
    elif (winner.group() == 'Dire'):
        result = 1

    duration = i.find_all('td')[3].get_text()

    radiant = i.find_all('td')[5]
    radiant_heroes_div = radiant.find_all('div')[0]
    radiant_heroes = radiant_heroes_div.find_all('img')

    team0 = []
    for radiant_teams in radiant_heroes:
        team0.append(radiant_teams.get('title'))

    dire = i.find_all('td')[5]
    dire_heroes_div = dire.find_all('div')[6]
    dire_heroes = dire_heroes_div.find_all('img')

    team1 = []
    for dire_teams in dire_heroes:
        team1.append(dire_teams.get('title'))

    matches.append(Match(result=result, radiant=team0, dire=team1, duration=duration))

for i, match in enumerate(matches):
    df.loc[i, 'Result'] = match.getResult()

for i, match in enumerate(matches):
    for hero in heroes[1:]:  # skip the first element, which is just the 'Result' column
        if hero in match.getRadiant():
            df.loc[i, hero] = 0
        elif hero in match.getDire():
            df.loc[i, hero] = 1
        else:
            df.loc[i, hero] = -1

df.to_csv('test_matches.csv', mode='a', index=True, header=False)
