def getgamemodeid(givengamemode):
    gamemode_dict = {
    'attrition': 'aitdm',
    'bounty hunt': 'at',
    'one in the chamber': 'chamber',
    'amped hardpoint': 'cp',
    'capture the flag': 'ctf',
    'frontier defense': 'fd',
    'free for all': 'ffa',
    'frontier war': 'fw',
    'gungame': 'gg',
    'infection': 'inf',
    'last titan standing': 'lts',
    'marked for death': 'mfd',
    'pilots vs. pilots': 'ps',
    'sticks and stones': 'sns',
    'skirmish': 'tdm',
    'titan brawl': 'ttdm'
    }
    gamemodeid = ""
    gamemode = ""
    for gamemode_in_dict in gamemode_dict:     
        if(givengamemode.lower().replace(" ", "") in gamemode_in_dict.lower().replace(" ", "")):     
            gamemodeid = gamemode_dict[gamemode_in_dict]
            gamemode = gamemode_in_dict
            break
    
    return gamemodeid, gamemode
