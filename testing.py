#how tf do i do this shit lmao
from flask import Flask,render_template,request
import webbrowser, sys, requests, bs4, selenium
import cgi
import cgitb; cgitb.enable()



app = Flask(__name__,template_folder='Templates')

@app.route('/send', methods=['GET','POST'])
def send():
    interminable_end = ""
    if request.method == 'POST':
        name1 = request.form['name1']
        name2=request.form['name2']
        event_id = [100378,100370,84999,87748,87131,86587,85902,86737,86005,87200,85698,91758,73485,88335,88344,89578,87321,88226,91762,85926,91678,92557,80427,78473,89027,85929,91608,87378,85778,10053,87073,87119,87914,84983,98010,88478,10299,96471,85341,96684,10246,97424,89197,96935,85809,10028,98684,88026,86222,88973,10223]
        tourn_id = [11772,11772,10038,10621,10180,10364,10192,10401,10210,10537,10161,11057,8739,10691,10692,10844,10560,10680,10615,10196,11050,11148,9432,9270,10768,10197,11044,10569,10171,11564,10512,10519,10646,10037,11652,10701,12159,11254,10081,11552,10864,11622,10796,11447,10181,11877,11722,10663,10274,10763,12082]
        tournament_storage = []
        results_storage = []
        for x in range (0,len(event_id)):
            website = 'https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=' + str(event_id[x]) + '&tourn_id=' + str(tourn_id[x])
            tabroomRes = requests.get(website)
            tabroomSoup = bs4.BeautifulSoup(tabroomRes.text, features="html.parser")
            tournament_name = tabroomSoup.select('div > h2[class="centeralign marno"]')
            urmom = None

            tabroomElems = tabroomSoup.select('td > a')
            checker = False
            for names in tabroomElems:
                if names.text.find(name1 + ' & ' + name2) != -1 or names.text.find(name2 + ' & ' + name1) != -1:
                    for elem in tournament_name:
                        print(elem.text)
                        tournament_storage.append(elem.text)
                    print('https://www.tabroom.com' + names.get('href'))
                    resultsPage = 'https://www.tabroom.com' + names.get('href')
                    checker = True
                    break
            if(checker == False):
                continue
            resultsPageRes = requests.get(resultsPage)
            resultsSoup = bs4.BeautifulSoup(resultsPageRes.text, features="html.parser")
            rowElems = resultsSoup.select('div > div[class="row"]')
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
                for inc in range(0, judgeVars[i]):
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

            # at tis point,we need to create two different lists. one has the tournament name
            # and the other has prelim wins and losses and outround wins and losses


            results_storage.append("Prelim wins: " + str(Wcount) + " Prelim losses: " + str(Lcount) + " Outround wins: " + str(outRoundWCount) + " Outround losses: " + str(outRoundLCount))
        print(tournament_storage)
        print(results_storage)
        return render_template('index3.html',len=len(tournament_storage),tournament_storage=tournament_storage,results_storage=results_storage, name1=name1,name2=name2)
    else:
        return render_template('testing.html')


if __name__ == "__main__":
    app.debug = True
    app.run()