import discord
import matplotlib.pyplot as plt
import numpy as np
import requests

def make_donut_chart(botmessage, playerid, server=""):
    plt.figure().clear()
    weapon = {
    "human_execution": "execution",
    "mp_weapon_car": "car",
    "mp_weapon_defender": "charge rifle",
    "mp_weapon_doubletake": "double take",
    "mp_weapon_epg": "epg",
    "mp_weapon_hemlok_smg": "volt",
    "mp_weapon_lstar": "lstar",
    "mp_weapon_r97": "r97",
    "mp_weapon_rspn101": "r-201",
    "mp_weapon_smart_pistol": "smart pistol",
    "mp_weapon_sniper": "kraber",
    "mp_weapon_vinson": "flatline",
    "mp_weapon_autopistol": "re-45 auto",
    "mp_weapon_alternator_smg": "alternator",
    "mp_weapon_frag_grenade": "frag grenade",
    "mp_weapon_g2": "g2",
    "mp_weapon_lmg": "spitfire",
    "mp_weapon_smr": "smr",
    "mp_weapon_softball": "softball",
    "mp_weapon_thermite_grenade": "firestar",
    "melee_pilot_emptyhanded": "melee",
    "mp_weapon_mastiff": "mastiff",
    "mp_weapon_mgl": "mgl",
    "mp_weapon_rspn101_og": "r-101",
    "mp_weapon_wingman": "wingman",
    "invalid": "invalid",
    "mp_weapon_arc_launcher": "thunderbolt",
    "mp_weapon_dmr": "dmr",
    "mp_weapon_grenade_electric_smoke": "electric smoke",
    "mp_weapon_pulse_lmg": "cold war",
    "mp_weapon_satchel": "satchel",
    "mp_weapon_shotgun": "eva-8 auto",
    "mp_weapon_shotgun_pistol": "mozambique",
    "mp_weapon_wingman_n": "wingman elite",
    "mp_weapon_grenade_gravity": "gravity star",
    "mp_weapon_grenade_sonar": "pulse blade",
    "mp_weapon_rocket_launcher": "archer",
    "outOfBounds": "outOfBounds",
    "mind_crime": "mind crime",
    "mp_weapon_esaw": "devotion",
    "fall": "fall",
    "mp_weapon_semipistol": "p2016",
    "mp_weapon_grenade_emp": "arc grenade",
    "mp_weapon_hemlok": "hemlok",
    "phase_shift": "phase shift"
    }

    if(server != "All"):
        payload = {'player': playerid, 'server': server}
    else:
        payload = {'player': playerid}

    response = requests.get('https://tone.sleepycat.date/v2/client/weapons', params=payload).json()

    labels = []
    values = []
    total = 0
    dict_weapon_with_kills = {}
    for i in response.keys():
        weaponstats = response[i]
        dict_weapon_with_kills[i] = weaponstats['kills']
        total += weaponstats['kills']

    other = 0
    for j in dict_weapon_with_kills:
        if(dict_weapon_with_kills[j] > total/20):
            try:
                labels.append(weapon[j])
            except KeyError:
                labels.append(j)
            values.append(dict_weapon_with_kills[j])
        else:
            other += dict_weapon_with_kills[j]

    labels.append("other")
    values.append(other)

    plt.style.use('ggplot')
    plt.title("weapons used by player")
    plt.pie(x=values, autopct='%.0f%%', startangle=90)
    plt.axis('equal')
    plt.legend(title="weapons" ,labels=labels, loc='upper left', bbox_to_anchor=(-0.17, 0.67, 0.5, 0.5))

    circle = plt.Circle(xy=(0,0), radius=.1, facecolor='white')
    plt.gca().add_artist(circle)

    plt.savefig("Reuse/images/player_weapons_used.png")
    img_file = discord.File("Reuse/images/player_weapons_used.png", filename="player_weapons_used.png")
    botmessage.set_image(url="attachment://player_weapons_used.png")

    return botmessage, img_file
