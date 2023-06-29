import requests

def valueschartgamemode(playerid, weaponid):

    payload = {'player': playerid, 'weapon': weaponid}
    response = requests.get('https://tone.sleepycat.date/v2/client/gamemodes', params=payload).json()

    gamemode_color = {'aitdm':(1, 0.0, 0.0),'at':(1, 0.375, 0.0),'chamber':(1, 0.75, 0.0),'cp':(0.875, 1, 0.0),'ctf':(0.5, 1, 0.0),'fd':(0.125, 1, 0.0),'ffa':(0.0, 1, 0.25),'fw':(0.0, 1, 0.625),'gg':(0.0, 1.0, 1),'inf':(0.0, 0.625, 1),'lts':(0.0, 0.25, 1),'mfd':(0.125, 0.0, 1),'ps':(0.5, 0.0, 1),'sns':(0.875, 0.0, 1), 'tdm':(1, 0.0, 0.75),'ttdm':(1, 0.0, 0.375), 'other': (1, 0.0, 1)}
    gamemode_dict = {'aitdm':'Attrition','at':'Bounty Hunt','chamber':'One in the Chamber','cp':'Amped Hardpoint','ctf':'Capture the Flag','fd':'Frontier Defense','ffa':'Free for All','fw':'Frontier War','gg':'GunGame','inf':'Infection','lts':'Last Titan Standing','mfd':'Marked for Death','ps':'Pilots Vs. Pilots','sns':'Sticks and Stones','tdm':'Skirmish','ttdm':'Titan Brawl'}

    labels = []
    values = []
    colors = []
    total = 0
    dict_gamemodes_with_kills = {}
    for i in response.keys():
        gamemodestats = response[i]
        dict_gamemodes_with_kills[i] = gamemodestats['kills']
        total += gamemodestats['kills']
    
    handler = lambda p : response[p]['kills']
    result = sorted(dict_gamemodes_with_kills, key=handler, reverse=True)

    other = 0
    for j in result:
        try:
            labels.append(gamemode_dict[j])
        except KeyError:
            labels.append(j)

        colors.append(gamemode_color[j])
        values.append(dict_gamemodes_with_kills[j])

    return labels, values, colors

