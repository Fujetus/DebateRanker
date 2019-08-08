from flask import Flask, render_template, request
import requests, bs4
import pandas
import os

app = Flask(__name__, template_folder='Templates')

@app.route('/', methods=['GET', 'POST'])
def send():
    interminable_end = ""
    if request.method == 'POST':
        # variable storge as well taking in the two last names
        name1 = request.form['name1'].strip()
        name2 = request.form['name2'].strip()
        event_id = [100378, 100370, 84999, 87748, 87131, 86587, 85902, 86737, 86005, 87200, 85698, 91758, 73485, 88335, 92194, 94405,
                    88344, 89578, 87321, 88226, 91762, 85926, 91678, 92557, 80427, 78473, 89027, 85929, 91608, 87378,
                    85778, 100539, 87073, 87119, 87914, 84983, 98010, 88478, 102992, 96471, 85341, 96684, 102463, 97424,
                    89197, 96935, 85809, 100286, 98684, 88026, 86222, 88973, 102231]
        tourn_id = [11772, 11772, 10038, 10621, 10180, 10364, 10192, 10401, 10210, 10537, 10161, 11057, 8739, 10691, 11109, 11335,
                    10692, 10844, 10560, 10680, 10615, 10196, 11050, 11148, 9432, 9270, 10768, 10197, 11044, 10569,
                    10171, 11564, 10512, 10519, 10646, 10037, 11652, 10701, 12159, 11254, 10081, 11552, 10864, 11622,
                    10796, 11447, 10181, 11877, 11722, 10663, 10274, 10763, 12082]
        prelim_wins = 0
        outround_wins = 0
        total_prelim = 0
        total_outround = 0
        tournament_storage = []
        results_storage = []
        tournament_url = []
        total_breaks = 0
        silverbid = 0;
        goldbidcounter = 0;

        f = open("/home/Fujetus/DebateWatch/Bids/BIDS.txt", "r")  # open file

        # keep iterating through lines until you get the right one
        text = "nonsense"
        while text != "":
            text = f.readline()
            if (text.upper().find(" " + name1.upper() + " ") != -1 and text.upper().find(" " + name2.upper() + ",") != -1 or text.upper().find(
                    " " + name2.upper() + " ") != -1 and text.upper().find(" " + name1.upper() + ",") != -1):
                if (name1 == name2):
                    index_of_ampersand = text.index("&")
                    if (text[0:index_of_ampersand].find(name1) != -1 and text[index_of_ampersand:text.__len__()].find(
                            name1) != -1):
                        break
                else:
                    break
        # make a string with a list of all their numbers
        if text.__len__() == 0:
            pass
        else:
            new_text = f.readline()
            while (new_text.find("&") == -1):
                text += new_text
                new_text = f.readline()

            # in a list like 0,1,0,2 we only care about 0 and 0. The fact that they are both 0 means there are two silver bids.
            # A non-zero value indicates a gold bid
            even = True  # this helps switch off every other number
            for elem in text:
                if (elem >= "0" and elem <= "9"):  # if the element we are looking at is a number
                    if even:  # if its one of the 0th, 2nd, 4th, etc element (the ones we care about)
                        if elem == "0":
                            silverbid += 1  # if 0, silver
                        else:
                            goldbidcounter += 1  # if not, gold
                        even = False
                    else:
                        even = True

        # running through all the url's for with the different event_id and tourn_id
        for x in range(0, len(event_id)):
            # souping the results page
            fh = open(('/home/Fujetus/DebateWatch/Tourneys/' + str(event_id[x]) + ".txt"), "r")
            tabroomSoup = bs4.BeautifulSoup(fh.read(), features="html.parser")
            tournament_name = tabroomSoup.select('div > h2[class="centeralign marno"]')
            # finding the two names and storing the tournament name
            tabroomElems = tabroomSoup.select('td > a')
            checker = False
            for names in tabroomElems:
                if names.text.strip().upper() == (name1.upper() + ' & ' + name2.upper()) or names.text.strip().upper() == (name2.upper() + ' & ' + name1.upper()):
                    for elem in tournament_name:
                        print(elem.text)
                        tournament_storage.append(elem.text)
                    print('https://www.tabroom.com' + names.get('href'))
                    resultsPage = 'https://www.tabroom.com' + names.get('href')
                    tournament_url.append('https://www.tabroom.com' + names.get('href'))
                    checker = True
                    break
            if (checker == False):
                continue
            # souping specifically the resuls page for the partnership
            resultsPageRes = requests.get(resultsPage)
            resultsSoup = bs4.BeautifulSoup(resultsPageRes.text, features="html.parser")
            rowElems = resultsSoup.select('div > div[class="row"]')
            listOfJudges = []
            completeList = []
            judgeVars = []
            judgeCounter = 0

            i = 0
            # storing the dubs and losses for prelims and outrounds
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
            breakFlag = False
            GMU_faggotry= False
            GMU_outround=False
            Churchill_faggotry=False
            i = 0
            if event_id[x] == 92194:
                GMU_faggotry = True
            if event_id[x] == 102992:
                Churchill_faggotry=True
            if not Churchill_faggotry:
                while i < len(completeList):
                    GMU_outround = False
                    # first condition checks for byes and second condition checks for coach overs, if true ignores
                    if rowElems[i].text.upper().find('\tBYE\n') != -1 or (judgeVars[i] == 0 and (rowElems[i].text.upper().find('\tPRO\n') or rowElems[i].text.upper().find('\tCON\n'))):
                        if rowElems[i].text.upper().find('ROUND') == -1:
                            breakFlag = True
                            pass
                    # checks if a round is an outround, adds to outround counters if true and defaults to prelim counters in the else statement
                    elif rowElems[i].text.upper().find('ROUND') == -1:
                        breakFlag = True
                        if completeList[i].count('W') > completeList[i].count('L'):
                            outRoundWCount += 1
                        else:
                            outRoundLCount += 1
                    else:
                        if(GMU_faggotry):
                            if completeList[i].count('W') + completeList[i].count('L') > 1:
                                GMU_outround= True
                        if completeList[i].count('W') > completeList[i].count('L'):
                            if(GMU_outround):
                                outRoundWCount+=1
                                breakFlag= True
                            else:
                                Wcount += 1
                        else:
                            if (GMU_outround):
                                outRoundLCount += 1
                                breakFlag= True
                            else:
                                Lcount += 1
                    i += 1
            else:
                while i < len(completeList):
                    # first condition checks for byes and second condition checks for coach overs, if true ignores
                    if rowElems[i].text.upper().find('\tBYE\n') != -1 or (judgeVars[i] == 0 and (rowElems[i].text.upper().find('\tPRO\n') or rowElems[i].text.upper().find('\tCON\n'))):
                        if rowElems[i].text.upper().find('ROUND') == -1:
                            breakFlag = True
                            pass
                    # checks if a round is an outround, adds to outround counters if true and defaults to prelim counters in the else statement
                    elif completeList[i].count('W') + completeList[i].count('L') > 1:
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

            if breakFlag:
                total_breaks += 1
            prelim_wins += Wcount
            total_prelim += (Wcount + Lcount)
            outround_wins += outRoundWCount
            total_outround += (outRoundWCount+outRoundLCount)
            # at tis point,we need to create two different lists. one has the tournament name
            # and the other has prelim wins and losses and outround wins and losses

            results_storage.append(
                "Prelim wins: " + str(Wcount) + "   Prelim losses:   " + str(Lcount) + "   Outround wins:   " + str(
                    outRoundWCount) + "   Outround losses:   " + str(outRoundLCount))
        if total_prelim == 0:
            return render_template("noRecord.html")
        prelim_percentage = "%.2f" % ((prelim_wins/total_prelim)*100)
        if total_outround == 0:
            outround_percentage = 0
        else:
            outround_percentage = "%.2f" %((outround_wins/total_outround)*100)
        break_percentage = "%.2f" % ((total_breaks/tournament_storage.__len__())*100)
        win_percentage = "%.2f" % ((prelim_wins + outround_wins)/(total_prelim + total_outround)*100)
        print(tournament_storage)
        print(results_storage)
        for elem in tournament_url:
            print(elem)
        # sending to the final html file with everything stored up
        return render_template('index3.html', len=len(tournament_storage), tournament_storage=tournament_storage,
                               results_storage=results_storage, name1=name1, name2=name2,prelim_percentage= prelim_percentage,
                               outround_percentage=outround_percentage,break_percentage=break_percentage, win_percentage=win_percentage,
                               w_l=str(prelim_wins + outround_wins)+'-'+str(total_prelim + total_outround - prelim_wins - outround_wins),
                               prelim_record=str(prelim_wins)+'-'+str(total_prelim - prelim_wins),outround_record=str(outround_wins)+'-'+str(total_outround - outround_wins),
                               breaks=str(total_breaks)+'-'+str(tournament_storage.__len__() - total_breaks),tournament_url=tournament_url,goldbidcounter=goldbidcounter,silverbid=silverbid)
    else:
        return render_template('testing.html')


# debugging and running flask
if __name__ == "__main__":
    app.debug = True
    app.run()
