import pandas as pd
import requests
from bs4 import BeautifulSoup
import openpyxl

#Creating year column:
y = 1929
years = []
years.append(y)
while y <= 2022:
    y += 1
    years.append(y)
df3 = pd.DataFrame(years, columns=['Year']) # years 1929-2023

# scraping data from tables in wikipedia articles on platinum/world level PSA Squash Events
elg = 'https://en.wikipedia.org/wiki/El_Gouna_International'
bto = 'https://en.wikipedia.org/wiki/British_Open_Squash_Championships'
hko = 'https://en.wikipedia.org/wiki/Hong_Kong_Open_(squash)'
qtc = 'https://en.wikipedia.org/wiki/Qatar_Classic'
wco = 'https://en.wikipedia.org/wiki/Windy_City_Open'
wsc = 'https://en.wikipedia.org/wiki/World_Squash_Championships'
uso = 'https://en.wikipedia.org/wiki/United_States_Open_(squash)'
toc = 'https://en.wikipedia.org/wiki/Tournament_of_Champions_(squash)'
wtf = 'https://en.wikipedia.org/wiki/PSA_World_Tour_Finals'

url_list = [wsc, wtf, bto, uso, toc, wco, hko, elg, qtc]
for k in range(len(url_list)):
    url = url_list[k]
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all("table")  # returns a list of tables

# index of tables(s) differs from article to article
    if url_list[k] == wsc:
        table_list = [tables[2]]
    elif url_list[k] == wtf:
        table_list = [tables[3]]
    elif url_list[k] == uso:
        table_list = [tables[1], tables[2], tables[3]]
    elif url_list[k] == toc:
        table_list = [tables[1], tables[3]]
    else:
        table_list = [tables[1]]

    new_year = []
    new_winner = []
    for i in range(len(table_list)):
        for row in table_list[i].find_all('tr')[1::]: # for each row in a table
            cells = row.find_all('td') # find all cells
            if len(cells) > 2: # rows with fewer than two cells indicate that the given year had no winner
                if cells[0].get_text().strip() == '2007 (October)': # measures for if two finals from different seasons
                    year = '2007'                                   # happened in the same year
                elif cells[0].get_text().strip() == '2007 (April)':
                    year = '2006'
                elif len(cells[0].get_text().strip()) == 7 and cells[0].get_text().strip()[-1] != ']': # getting rid of bracketed Wikipedia citations next to names
                    year = cells[0].get_text().strip()[0:2] + cells[0].get_text().strip()[-2::]
                elif cells[0].get_text().strip()[-1] == ']': # see above comment
                    year = cells[0].get_text().strip()[0:4]
                else:
                    year = cells[0].get_text().strip()
                if url_list[k] == wsc:
                    winner = cells[2].get_text().strip() # World Champs page has location in col 1, winner in col 2
                elif url_list[k] == wtf: # fixing issue that cells in location col have different heights
                    rows = soup.find_all('tr')
                    header_index = -1
                    headers = rows[0].find_all('th')
                    for idx, header in enumerate(headers):
                        if header.text.strip() == 'Champion':
                            header_index = idx
                    if len(cells) > header_index:
                        champion_cell = cells[header_index - 2]
                        winner = champion_cell.text[:-6]
                elif url_list[k] == toc:
                    winner = cells[1].get_text().strip()
                    if cells[1].get_text().strip()[-1] == ']': # removing bracketed Wikipedia citations
                        winner = cells[1].get_text().strip()[:-3]
                    if winner[-1] == '[':
                        winner = winner[:-1]
                else:
                    winner = cells[1].get_text().strip()
                new_winner.append(winner) # create list of winners
                new_year.append(int(year)) # create list of integer years in which the event has held



    new_col = []
    for m in range(len(years)):
        for j in range(len(new_year)):
            if years[m] == new_year[j]: # if there is a match between event year and list of all years
                new_col.append(new_winner[j]) # insert winner into new list
        if years[m] not in new_year: # if there is a year in 'years' where the event was not held
            new_col.append('') # put a blank, indicating that there was no winner in that year

    # dictionary linking url to tournament name
    titles = {elg: 'ElGouna', bto: 'BritishOpen', hko: 'HongKong', qtc: 'QatarClassic', wco: 'WindyCity',
              wsc: 'WorldChamps', uso: 'USOpen', toc: 'ToC', wtf: 'WorldTourFinals'}

    df3[titles[url_list[k]]] = new_col
    df3.at[81, 'WorldTourFinals'] = ''

# Displaying all columns and rows, printing dataframe
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df3)


