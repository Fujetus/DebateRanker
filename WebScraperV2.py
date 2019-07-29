import webbrowser, sys, requests, bs4, selenium

name1 = 'Chandrashekhar'
name2 = 'Jain'
website = 'https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=98684&tourn_id=11722'

tabroomRes = requests.get(website)

tabroomSoup = bs4.BeautifulSoup(tabroomRes.text, features="html.parser")

# creates Res object that gives us Tabroom page for a specific tournament. Then, we set it up for parsing.

tabroomElems = tabroomSoup.select('td > a')

# td > a gives entire element for each team


# Going from PF Results Page to Specific Pairing Results Page
for names in tabroomElems:
    if names.text.find(name1 + ' & ' + name2) != -1 or names.text.find(name2 + ' & ' + name1) != -1:
        print('https://www.tabroom.com' + names.get('href'))
        resultsPage = 'https://www.tabroom.com' + names.get('href')
        # resultsPage sends you to team's record page

resultsPageRes = requests.get(resultsPage)

resultsSoup = bs4.BeautifulSoup(resultsPageRes.text, features="html.parser")

rowElems = resultsSoup.select('div > div[class="row"]')

# for elems in rowElems:
    # print(elems.text.strip())
# gives a list of integers that delegate dubs and Ls to each round
listOfJudges = []
completeList = []
judgeVars = []
judgeCounter = 0

i = 0

while i < len(rowElems):
    judgeCounter = 0
    listOfJudges = rowElems[i].select('span > a[class="white padtop padbottom"]')
    for elems in listOfJudges:
        if elems.get('href').find('judge.mhtml') != -1:
            judgeCounter += 1
    judgeVars.append(judgeCounter)
    i += 1
# for elems in judgeVars:
    # print(elems)

roundsElems = resultsSoup.select('div > span[class="tenth semibold"]')

dubsElems = resultsSoup.select('div > span[class="tenth centeralign semibold"]')

i = 0
dubsIncrement = 0
dubsChunk = ''
while i < len(judgeVars):
    for inc in range(0,judgeVars[i]):
        dubsChunk += dubsElems[dubsIncrement].text.strip()
        dubsIncrement += 1
    completeList.append(roundsElems[i].text.strip() + ' ' + dubsChunk)
    dubsChunk = ''
    i += 1
for elems in completeList:
    print(elems)

outRoundWCount = 0
outRoundLCount = 0
Wcount = 0
Lcount = 0
i = 0
while i < len(completeList):
    if rowElems[i].text.find('Bye') != -1:
        print()
    elif completeList[i].upper().find('ROUND') == -1:
        if completeList[i].count('W') > completeList[i].count('L'):
            outRoundWCount += 1
        else:
            outRoundLCount += 1
    else:
        if completeList[i].count('W') == 1:
            Wcount += 1
        else:
            Lcount += 1
    i += 1

print('Prelim Wins: ' + str(Wcount))
print('Prelim Losses: ' + str(Lcount))
print('Outround Wins: ' + str(outRoundWCount))
print('Outround Losses: ' + str(outRoundLCount))
