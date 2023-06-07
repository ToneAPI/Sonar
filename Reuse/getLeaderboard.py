import datetime
from PIL import Image, ImageDraw, ImageFont
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

    counter = 1
    message = ""
    for p in result:
        message = message + str(f"{str(counter):<2} | ") + str(f"{response[p]['username']:<18}:") + str(f'{str(round(handler(p), 1)):<6}' + f"{str(' ' + board.replace('_', ' '))}\n")
        counter= counter+1 

    return message


def create_leaderboard_image(board:str, weaponid="", weaponname="", server=""):
    message = getleaderboard(board, weaponid, weaponname, server)
    image_width = 600
    image_height = 300
    background_color = (43, 45, 49) 

    font_size = 24
    font_color = (255, 255, 255)  
    monospace_font_path = r'Sonar\Reuse\Fonts\GTAmericaMono.ttf'

    image = Image.new('RGB', (image_width, image_height), background_color)

    font = ImageFont.truetype(monospace_font_path, font_size)

    draw = ImageDraw.Draw(image)

    text_width, text_height = draw.textsize(message, font=font)

    text_x = (image_width - text_width) // 2
    text_y = (image_height - text_height) // 2

    draw.text((text_x, text_y), message, font=font, fill=font_color)

    image.save('Reuse/images/leaderboard.png')

def create_leaderboard_message(board:str, weaponid="", weaponname="", server=""):
    #create_leaderboard_image(board, weaponid, weaponname, server)
    message = getLeaderboard(board, weaponid, weaponname, server)
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

    date_time = datetime.datetime.utcnow()
    time = str(date_time)[11:16]
    date = str(date_time)[0:10]
    #img_file = discord.File("Reuse/images/leaderboard.png", filename="leaderboard.png")
    #botmessage.set_image(url="attachment://leaderboard.png")
    botmessage.add_field(name="", value=message)
    botmessage.set_footer(text=f"Brought to you by ToneAPI, created at {date} on {time}")

    return botmessage, img_file
