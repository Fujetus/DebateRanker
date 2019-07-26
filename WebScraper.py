import webbrowser, sys, requests, bs4, selenium
from typing import List, Any

jaintardRes = requests.get('https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=87073&tourn_id=10512')

tardSoup = bs4.BeautifulSoup(jaintardRes.text, features="html.parser")

tardElems = tardSoup.select('td > a')

# Going from PF Results Page to Specific Pairing Results Page
for names in tardElems:
    if names.text.find('Chandrashekhar & Jain') != -1:
        print('https://www.tabroom.com' + names.get('href'))
        resultsPage = 'https://www.tabroom.com' + names.get('href')

resultsPageRes = requests.get(resultsPage)

resultsSoup = bs4.BeautifulSoup(resultsPageRes.text, features="html.parser")

dubsElems = resultsSoup.select('div > span[class="tenth centeralign semibold"]')
for Ws in dubsElems:
    print(Ws.text.upper().strip())


roundsElems = resultsSoup.select('div > span[class="tenth semibold"]')
for rounds in roundsElems:
    print(rounds.text.upper().strip())

i = 0
dubCounter = 0
newBalance = []
while len(roundsElems) > i & len(dubsElems) > dubCounter:
    if(roundsElems[i].text.upper().strip().find('ROUND')) != -1:
        newBalance.append(roundsElems[i].text + ' ' + dubsElems[dubCounter].text)
        i += 1
        dubCounter += 1
    else:
        newBalance.append(roundsElems[i].text + ' ' + dubsElems[dubCounter].text + dubsElems[dubCounter+1].text + dubsElems[dubCounter+2].text)
        i += 1
        dubCounter += 3

for elems in newBalance:
    print(len(roundsElems))


print(len(roundsElems))


