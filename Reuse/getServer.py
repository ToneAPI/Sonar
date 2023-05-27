import aiohttp


async def getserver(snippet):
        server = ""
        async with aiohttp.ClientSession() as session:
            async with session.get('https://tone.sleepycat.date/v2/client/servers') as r:
                response = await r.json()
                servers = response.keys()
        for i in servers:
            if(snippet.lower().replace(" ", "") == i.lower().replace(" ", "")):
                server = i
                break
            elif(snippet.lower().replace(" ", "") in i.lower().replace(" ", "")):
                 server = i

        return server