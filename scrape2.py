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
df3 = pd.DataFrame(years, columns=['Year'])

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
        for row in table_list[i].find_all('tr')[1::]:
            cells = row.find_all('td')
            if len(cells) > 2:
                if cells[0].get_text().strip() == '2007 (October)':
                    year = '2007'
                elif cells[0].get_text().strip() == '2007 (April)':
                    year = '2006'
                elif len(cells[0].get_text().strip()) == 7 and cells[0].get_text().strip()[-1] != ']':
                    year = cells[0].get_text().strip()[0:2] + cells[0].get_text().strip()[-2::]
                elif cells[0].get_text().strip()[-1] == ']':
                    year = cells[0].get_text().strip()[0:4]
                else:
                    year = cells[0].get_text().strip()
                if url_list[k] == wsc:
                    winner = cells[2].get_text().strip()
                elif url_list[k] == wtf: # I don't know how the fuck this shit works
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
                    if cells[1].get_text().strip()[-1] == ']':
                        winner = cells[1].get_text().strip()[:-3]
                    if winner[-1] == '[':
                        winner = winner[:-1]
                else:
                    winner = cells[1].get_text().strip()
                new_winner.append(winner)
                new_year.append(int(year))



    new_col = []
    for m in range(len(years)):
        for j in range(len(new_year)):
            if years[m] == new_year[j]:
                new_col.append(new_winner[j])
        if years[m] not in new_year:
            new_col.append('')

    titles = {elg: 'ElGouna', bto: 'BritishOpen', hko: 'HongKong', qtc: 'QatarClassic', wco: 'WindyCity',
              wsc: 'WorldChamps', uso: 'USOpen', toc: 'ToC', wtf: 'WorldTourFinals'}

    df3[titles[url_list[k]]] = new_col
    df3.at[81, 'WorldTourFinals'] = ''

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
print(df3)


