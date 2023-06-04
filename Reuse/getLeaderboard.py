import requests

def getleaderboard(board:str, weaponid="", weaponname="", server=""):
    payload = {"weapon": weaponid, "server": server}
    response = requests.get('https://tone.sleepycat.date/v2/client/players', params=payload).json()
    players = response.keys()
    if(board.lower() == "totald"):
        board = "total_distance"
    elif(board.lower() == "maxd"):
        board = "max_distance"
        
    if(board.lower() == "kd"):
        handler = lambda p : response[p]['kills'] / max(response[p]["deaths"], 1)
    elif(board.lower() == "avgd"):
        handler = lambda p : response[p]['total_distance'] / max(response[p]["kills"], 1)
    else:
        if(board.lower() not in ['username', 'deaths','kills', 'max_distance','total_distance']):
            raise KeyError("Key " + board.lower() + ' not found for player leaderboard')
        handler = lambda p : response[p][board.lower()]
            
    result = sorted(players, key=handler, reverse=True)[:10]

    if(board.lower() == "deaths"):
        inbetween = "to"
    else:
        inbetween = "with"

    if(server == ""):
        server = "all servers"
    if(weaponname == ""):
        weaponname = "any weapon"

    botmessage = str(f"Leaderboard of {board} {inbetween} {weaponname} for {server}\n-------------------------------\n")

    counter = 1
    for p in result:
        botmessage = botmessage + str(f"{str(counter):<2}"+ " - " + f"{response[p]['username'] :<20}" + " : "+ f"{str(handler(p)):<8}" + "\n")
        counter= counter+1 

    return botmessage