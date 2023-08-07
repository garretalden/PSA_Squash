import pandas as pd
import requests
from bs4 import BeautifulSoup
import openpyxl

#Creating year columns
y = 1929
years = []
years.append(y)
while y <= 2022:
    y += 1
    years.append(y)
df = pd.DataFrame(years, columns=['Year'])

# British open
url_list = ['https://en.wikipedia.org/wiki/El_Gouna_International',
'https://en.wikipedia.org/wiki/British_Open_Squash_Championships',
            'https://en.wikipedia.org/wiki/Hong_Kong_Open_(squash)',
            'https://en.wikipedia.org/wiki/Qatar_Classic',
            'https://en.wikipedia.org/wiki/Windy_City_Open']

for k in range(len(url_list)):
    response = requests.get(url_list[k])
    soup = BeautifulSoup(response.content, 'html.parser')

    tables = soup.find_all("table")  # returns a list of tables
    table = tables[1]
    new_year = []
    new_winner = []
    for row in table.find_all('tr')[1::]:
        cells = row.find_all('td')
        if len(cells) > 2:
            if cells[0].get_text().strip() == '2007 (October)':
                year = '2007'
            elif cells[0].get_text().strip() == '2007 (April)':
                year = '2006'
            else:
                year = cells[0].get_text().strip()
            winner = cells[1].get_text().strip()
            new_winner.append(winner)
            new_year.append(int(year))

    new_col = []
    for i in range(len(years)):
        for j in range(len(new_year)):
            if years[i] == new_year[j]:
                new_col.append(new_winner[j])
        if years[i] not in new_year:
            new_col.append('')
    if k == 0:
        df['ElGouna'] = new_col
    if k == 1:
        df['BritishOpen'] = new_col
    if k == 2:
        df['HongKong'] = new_col
    if k == 3:
        df['QatarClassic'] = new_col
    if k == 4:
        df['WindyCity'] = new_col

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
#print(worlds_year)
#print(worlds_winner)


new_worlds = []
for i in range(len(years)):
    for j in range(len(worlds_year)):
        if years[i] == worlds_year[j]:
            new_worlds.append(worlds_winner[j])
    if years[i] not in worlds_year:
        new_worlds.append('')
df['WorldChamps'] = new_worlds

# US Open
url = 'https://en.wikipedia.org/wiki/United_States_Open_(squash)'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all("table")  # returns a list of tables
table_list = [tables[1], tables[2], tables[3]]
uso_year = []
uso_winner = []
for i in range(len(table_list)):
    for row in table_list[i].find_all('tr')[1::]:
        cells = row.find_all('td')
        if len(cells) > 2:
            if len(cells[0].get_text().strip()) == 4:
                year = cells[0].get_text().strip()
            elif len(cells[0].get_text().strip()) == 7:
                year = cells[0].get_text().strip()[0:2] + cells[0].get_text().strip()[-2::]
            winner = cells[1].get_text().strip()
            uso_year.append(int(year))
            uso_winner.append(winner)
#print(uso_year)
#print(uso_winner)


new_uso = []
for i in range(len(years)):
    for j in range(len(uso_year)):
        if years[i] == uso_year[j]:
            new_uso.append(uso_winner[j])
    if years[i] not in uso_year:
        new_uso.append('')
df['USOpen'] = new_uso

# JPM ToC
url = 'https://en.wikipedia.org/wiki/Tournament_of_Champions_(squash)'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

tables = soup.find_all("table")  # returns a list of tables
table_list = [tables[1], tables[3]]
toc_year = []
toc_winner = []
for i in range(len(table_list)):
    for row in table_list[i].find_all('tr')[1::]:
        cells = row.find_all('td')
        if len(cells) > 2:
            if len(cells[0].get_text().strip()) == 4:
                year = cells[0].get_text().strip()
            elif len(cells[0].get_text().strip()) == 7:
                year = cells[0].get_text().strip()[0:2] + cells[0].get_text().strip()[-2::]
            winner = cells[1].get_text().strip()
            toc_year.append(int(year))
            toc_winner.append(winner)

new_toc = []
for i in range(len(years)):
    for j in range(len(toc_year)):
        if years[i] == toc_year[j]:
            new_toc.append(toc_winner[j])
    if years[i] not in toc_year:
        new_toc.append('')
df['ToC'] = new_toc

# World Tour Finals
url = 'https://en.wikipedia.org/wiki/PSA_World_Tour_Finals'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
#print(soup.prettify())

tables = soup.find_all("table")  # returns a list of tables
table = tables[3]
wtf_year = []
wtf_winner = []
for i in range(len(table_list)):
    for row in table_list[i].find_all('tr')[1::]:
        cells = row.find_all('td')
        if len(cells) > 2:
            year = cells[0].get_text().strip()
            winner = cells[2].get_text().strip()
            wtf_year.append(int(year))
            wtf_winner.append(winner)

#print(wtf_year)
#print(wtf_winner)

new_wtf = []
for i in range(len(years)):
    for j in range(len(wtf_year)):
        if years[i] == wtf_year[j]:
            new_wtf.append(wtf_winner[j])
    if years[i] not in wtf_year:
        new_wtf.append('')
#print(new_wtf)

#df['WorldTourFinals'] = new_wtf

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
#print(df)

#df.to_excel("squash_test1.xlsx")

