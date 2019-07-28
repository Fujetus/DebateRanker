import webbrowser, sys, requests, bs4, selenium
import cgi
import cgitb; cgitb.enable()

name1 = 'Chandrashekhar'
name2 = 'Jain'
website = 'https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=87073&tourn_id=10512'

tabroomRes = requests.get('https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=87073&tourn_id=10512')

tabroomSoup = bs4.BeautifulSoup(tabroomRes.text, features="html.parser")

#creates Res object that gives us Tabroom page for a specific tournament. Then, we set it up for parsing.

tabroomElems = tabroomSoup.select('td > a')

# td > a gives entire element for each team



# Going from PF Results Page to Specific Pairing Results Page
for names in tabroomElems:
   if names.text.find(name1 + ' & ' + name2) != -1 or names.text.find(name2 + ' & ' + name1) != -1:
        print('https://www.tabroom.com' + names.get('href'))
        resultsPage = 'https://www.tabroom.com' + names.get('href')
        #resultsPage sends you to team's record page

resultsPageRes = requests.get(resultsPage)

resultsSoup = bs4.BeautifulSoup(resultsPageRes.text, features="html.parser")

dubsElems = resultsSoup.select('div > span[class="tenth centeralign semibold"]')
# for letters in dubsElems:
    # print(letters.text.upper().strip())

#prints LWLWLWLWLWLWL


roundsElems = resultsSoup.select('div > span[class="tenth semibold"]')
# for rounds in roundsElems:
    # print(rounds.text.upper().strip())

#prints all  name titles

i = 0
dubCounter = 0
completeList = []
while len(roundsElems) > i and len(dubsElems) > dubCounter:
    if(roundsElems[i].text.upper().strip().find('ROUND')) != -1:
        completeList.append(roundsElems[i].text.strip() + ' ' + dubsElems[dubCounter].text.strip())
        i += 1
        dubCounter += 1
    else:
        completeList.append(roundsElems[i].text.strip() + ' ' + dubsElems[dubCounter].text.strip() + dubsElems[dubCounter+1].text.strip() + dubsElems[dubCounter+2].text.strip())
        i += 1
        dubCounter += 3

for elems in completeList:
    print(elems)
    
Wcount = 0
Lcount = 0
i = 0
while i < len(completeList):
    if completeList[i].upper().find('ROUND') == -1:
        if completeList[i].count('W') == 2:
            Wcount += 1
        else:
            Lcount += 1
    else:
        if completeList[i].count('W') == 1:
            Wcount += 1
        else:
            Lcount += 1
    i += 1

print('Overall Wins: ' + str(Wcount))
print('Overall Losses: ' + str(Lcount))



