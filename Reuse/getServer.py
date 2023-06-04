async def getserver(s,snippet):
    server = ""
    async with s.get('https://tone.sleepycat.date/v2/client/servers') as r:
        response = await r.json()
        servers = response.keys()
        for i in servers:
            if(snippet.lower().replace(" ", "") == i.lower().replace(" ", "")):
                server = i
                break
            elif(snippet.lower().replace(" ", "") in i.lower().replace(" ", "")):
                 server = i

        return server