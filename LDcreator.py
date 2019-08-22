import requests,bs4
#11877 10028

event_id = [87320,86220,73480,89193,78471,87328,88024,97269,87648,87117,89366,87747,96683,85889,85326,85696,100283,87129,85928,85342,96937,85897,85779,86603,99675,81809,91587,92555,95124,88473,98038,100484,84981,96485,97355,97426,85919,87371,85318,102474,88970,87071,84998,98683,102988]
tourn_id = [10560,10274,8739,10796,9270,10561,10663,11584,10610,10519,10813,10621,11552,10173,10101,10161,11877,10180,10197,10081,11447,10192,10171,10364,11784,9578,11044,11148,11400,10701,11652,11564,10037,11529,11616,11622,10196,10569,10099,10864,10763,10512,10038,11722,12159]
for x in range (0,len(event_id)):
    website = 'https://www.tabroom.com/index/tourn/results/ranked_list.mhtml?event_id=' + str(event_id[x]) + '&tourn_id=' + str(tourn_id[x])
    tabroomRes = requests.get(website)
    tabroomSoup = bs4.BeautifulSoup(tabroomRes.text, features="html.parser")
    tournament_name = tabroomSoup.select('div > h2[class="centeralign marno"]')
    fh = open(str(event_id[x]) + '.txt', 'w')
    fh.write(tabroomRes.text)
    fh.close()