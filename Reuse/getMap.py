def getmapid(givenmap):
    map_dict = {"angel city": "angel_city",	
    "black water canal":"black_water_canal",	
    "coliseum":"coliseum",	
    "pillars": "coliseum_column",	
    "colony":"colony02",	
    "complex":"complex3",	
    "crashsite":"crashsite3",	
    "drydock":"drydock",	
    "eden":"eden",	
    "forwardbase kodai":"forwardbase_kodai",	
    "glitch":"glitch",	
    "boomtown":"grave",
    "homestead":"homestead",
    "deck":"lf_deck",	
    "meadow": "lf_meadow",
    "stacks":"lf_stacks",
    "township":"lf_township",
    "trafic":"lf_traffic",	
    "uma":"lf_uma",	
    "relic":"relic02",	
    "rise":"rise",	
    "exoplanet":"thaw",	
    "wargames":"wargames"}
    mapid = ""
    mapname = ""
    for mapname_in_dict in map_dict:     
        if(givenmap.lower().replace(" ", "") in mapname_in_dict.lower().replace(" ", "")):     
            mapid = map_dict[mapname_in_dict]
            mapname = mapname_in_dict
            break

    return mapid, mapname

