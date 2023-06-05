import asyncio

async def get_all_playerids(s, playernames):
     players = {}
     residue = []
     tasks = []
     for playername in playernames:
          task = asyncio.create_task(getplayerid(s, playername),name=playername)
          tasks.append(task)
     res = await asyncio.gather(*tasks)
     for player in res:
           player = player.split(":")
           playername = player[0].strip()
           playerid = player[1].strip()
           if(playerid != "None" and playername not in players):
                players[playername] = playerid
           else:
                residue.append(playername) 
     return players, residue

async def getplayerid(s,playername):
        playerid = ""
        playername = playername.replace(",", "")
        payload = str(f"?username={playername}")
        async with s.get(f'https://northstar.tf/accounts/lookup_uid{payload}') as r:
                
                response = await r.json()
                if (response['matches'] != None and response['matches'] != []):
                    playerid = response['matches'][0]
                    player = str(f"{playername.lower()}: {playerid}")
                else:
                    player = str(f"{playername.lower()}: {None}")
                return player