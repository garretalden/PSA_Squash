import pandas as pd
import requests
from bs4 import BeautifulSoup
import openpyxl
from scrape2 import years

# World championships
url = 'https://en.wikipedia.org/wiki/World_Squash_Championships'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all("table")  # returns a list of tables
table = tables[2]
worlds_year = []
worlds_winner = []
for row in table.find_all('tr')[1::]:
    cells = row.find_all('td')
    if len(cells) > 2:
        if len(cells[0].get_text().strip()) == 4:
            year = cells[0].get_text().strip()
        elif len(cells[0].get_text().strip()) == 7:
            year = cells[0].get_text().strip()[0:2] + cells[0].get_text().strip()[-2::]
        winner = cells[2].get_text().strip()
        worlds_year.append(int(year))
        worlds_winner.append(winner)
print(worlds_year)
print(worlds_winner)
