import discord
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

    if(server == ""):
        server = "all"
    if(weaponname == ""):
        weaponname = "any"

    botmessage = discord.Embed(title=f"Leaderboard of {board}", description=f"**Server:** {server}\n**Weapon:** {weaponname}", colour=discord.Colour.orange())    
    if(weaponname != "any"):
        if(requests.head(f"https://toneapi.github.io/ToneAPI_webclient/weapons/{weaponid}.png").status_code == 200):
            botmessage.set_thumbnail(url=f"https://toneapi.github.io/ToneAPI_webclient/weapons/{weaponid}.png")
        else:
            botmessage.set_thumbnail(url="https://toneapi.github.io/ToneAPI_webclient/weapons/notfound.png")

    counter = 1
    for p in result:
        botmessage.add_field(name="", value=str(str(f"**{str(counter):<2} |** " + f"**{response[p]['username']}" + ":** ") + f'{str(round(handler(p), 1))}' + f"{str(' ' + board.replace('_', ' '))}"), inline=False)
        counter= counter+1 

    return botmessage
