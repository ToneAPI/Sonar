import discord
from matplotlib import patheffects
import matplotlib.pyplot as plt
import numpy as np
import requests

def make_donut_chart(botmessage, playerid, server=""):
    plt.figure().clear()
    weapon_color = {'auto_titan_melee': (1, 0.05084745762711862, 0.0), 'bubble_shield': (1, 0.10169491525423724, 0.0), 'burn': (1, 0.15254237288135597, 0.0), 'crushed': (1, 0.2033898305084746, 0.0), 'damagedef_crush': (1, 0.2542372881355932, 0.0), 'damagedef_fd_explosive_barrel': (1, 0.30508474576271194, 0.0), 'damagedef_fd_tether_trap': (1, 0.35593220338983045, 0.0), 'damagedef_frag_drone_throwable_PLAYER': (1, 0.4067796610169492, 0.0), 'damagedef_nuclear_core': (1, 0.4576271186440678, 0.0), 'damagedef_suicide': (1, 0.5084745762711864, 0.0), 'damagedef_titan_fall': (1, 0.5593220338983051, 0.0), 'damagedef_titan_hotdrop': (1, 0.6101694915254238, 0.0), 'damagedef_titan_step': (1, 0.6610169491525424, 0.0), 'damagedef_unknown': (1, 0.711864406779661, 0.0), 'fall': (1, 0.7627118644067796, 0.0), 'human_execution': (1, 0.8135593220338984, 0.0), 'invalid': (1, 0.864406779661017, 0.0), 'melee_pilot_arena': (1, 0.9152542372881356, 0.0), 'melee_pilot_emptyhanded': (1, 0.9661016949152541, 0.0), 'melee_pilot_kunai': (0.9830508474576272, 1, 0.0), 'melee_pilot_sword': (0.9322033898305084, 1, 0.0), 'melee_titan_punch_ion': (0.8813559322033897, 1, 0.0), 'melee_titan_punch_legion': (0.8305084745762712, 1, 0.0), 'melee_titan_punch_northstar': (0.7796610169491525, 1, 0.0), 'melee_titan_punch_scorch': (0.728813559322034, 1, 0.0), 'melee_titan_punch_tone': (0.6779661016949152, 1, 0.0), 'melee_titan_punch_vanguard': (0.6271186440677967, 1, 0.0), 'melee_titan_sword': (0.576271186440678, 1, 0.0), 'mind_crime': (0.5254237288135593, 1, 0.0), 'mp_titanability_laser_trip': (0.47457627118644075, 1, 0.0), 'mp_titanability_slow_trap': (0.4237288135593218, 1, 0.0), 'mp_titanability_smoke': (0.3728813559322033, 1, 0.0), 'mp_titancore_amp_core': (0.3220338983050848, 1, 0.0), 'mp_titancore_flame_wave': (0.27118644067796605, 1, 0.0), 'mp_titancore_flame_wave_secondary': (0.22033898305084754, 1, 0.0), 'mp_titancore_laser_cannon': (0.1694915254237288, 1, 0.0), 'mp_titancore_nuke_missile': (0.1186440677966103, 1, 0.0), 'mp_titancore_salvo_core': (0.06779661016949179, 1, 0.0), 'mp_titancore_shift_core': (0.016949152542372836, 1, 0.0), 'mp_titanweapon_arc_cannon': (0.0, 1, 0.03389830508474567), 'mp_titanweapon_arc_wave': (0.0, 1, 0.08474576271186463), 'mp_titanweapon_barrage_core_launcher': (0.0, 1, 0.13559322033898313), 'mp_titanweapon_brute4_quad_rocket': (0.0, 1, 0.18644067796610164), 'mp_titanweapon_dumbfire_rockets': (0.0, 1, 0.2372881355932206), 'mp_titanweapon_flame_wall': (0.0, 1, 0.2881355932203391), 'mp_titanweapon_flightcore_rockets': (0.0, 1, 0.3389830508474576), 'mp_titanweapon_heat_shield': (0.0, 1, 0.3898305084745761), 'mp_titanweapon_laser_lite': (0.0, 1, 0.4406779661016951), 'mp_titanweapon_leadwall': (0.0, 1, 0.4915254237288136), 'mp_titanweapon_meteor': (0.0, 1, 0.5423728813559321), 'mp_titanweapon_meteor_thermite': (0.0, 1, 0.593220338983051), 'mp_titanweapon_particle_accelerator': (0.0, 1, 0.6440677966101696), 'mp_titanweapon_predator_cannon': (0.0, 1, 0.6949152542372881), 'mp_titanweapon_rocketeer_rocketstream': (0.0, 1, 0.7457627118644066), 'mp_titanweapon_salvo_rockets': (0.0, 1, 0.7966101694915251), 'mp_titanweapon_shoulder_rockets': (0.0, 1, 0.847457627118644), 'mp_titanweapon_sniper': (0.0, 1, 0.8983050847457625), 'mp_titanweapon_sticky_40mm': (0.0, 1, 0.9491525423728815), 'mp_titanweapon_stun_laser': (0.0, 1.0, 1), 'mp_titanweapon_tracker_rockets': (0.0, 0.9491525423728815, 1), 'mp_titanweapon_vortex_shield': (0.0, 0.898305084745763, 1), 'mp_titanweapon_vortex_shield_ion': (0.0, 0.8474576271186436, 1), 'mp_titanweapon_xo16_shorty': (0.0, 0.7966101694915251, 1), 'mp_titanweapon_xo16_vanguard': (0.0, 0.7457627118644066, 1), 'mp_weapon_alternator_smg': (0.0, 0.6949152542372881, 1), 'mp_weapon_arc_launcher': (0.0, 0.6440677966101696, 1), 'mp_weapon_arena3': (0.0, 0.5932203389830506, 1), 'mp_weapon_autopistol': (0.0, 0.5423728813559321, 1), 'mp_weapon_car': (0.0, 0.4915254237288136, 1), 'mp_weapon_defender': (0.0, 0.4406779661016951, 1), 'mp_weapon_dmr': (0.0, 0.38983050847457656, 1), 'mp_weapon_doubletake': (0.0, 0.3389830508474576, 1), 'mp_weapon_epg': (0.0, 0.2881355932203391, 1), 'mp_weapon_esaw': (0.0, 0.2372881355932206, 1), 'mp_weapon_frag_grenade': (0.0, 0.1864406779661021, 1), 'mp_weapon_g2': (0.0, 0.13559322033898358, 1), 'mp_weapon_grenade_electric_smoke': (0.0, 0.08474576271186418, 1), 'mp_weapon_grenade_emp': (0.0, 0.03389830508474567, 1), 'mp_weapon_grenade_gravity': (0.016949152542372836, 0.0, 1), 'mp_weapon_grenade_sonar': (0.06779661016949134, 0.0, 1), 'mp_weapon_gunship_turret': (0.11864406779660985, 0.0, 1), 'mp_weapon_hemlok': (0.16949152542372925, 0.0, 1), 'mp_weapon_hemlok_smg': (0.22033898305084776, 0.0, 1), 'mp_weapon_lmg': (0.27118644067796627, 0.0, 1), 'mp_weapon_lstar': (0.3220338983050848, 0.0, 1), 'mp_weapon_mastiff': (0.3728813559322033, 0.0, 1), 'mp_weapon_mgl': (0.4237288135593218, 0.0, 1), 'mp_weapon_peacekraber': (0.4745762711864412, 0.0, 1), 'mp_weapon_pulse_lmg': (0.5254237288135588, 0.0, 1), 'mp_weapon_r97': (0.5762711864406782, 0.0, 1), 'mp_weapon_rocket_launcher': (0.6271186440677958, 0.0, 1), 'mp_weapon_rspn101': (0.6779661016949152, 0.0, 1), 'mp_weapon_rspn101_og': (0.7288135593220337, 0.0, 1), 'mp_weapon_satchel': (0.7796610169491522, 0.0, 1), 'mp_weapon_semipistol': (0.8305084745762707, 0.0, 1), 'mp_weapon_shotgun': (0.8813559322033901, 0.0, 1), 'mp_weapon_shotgun_pistol': (0.9322033898305087, 0.0, 1), 'mp_weapon_smart_pistol': (0.9830508474576272, 0.0, 1), 'mp_weapon_smr': (1, 0.0, 0.9661016949152543), 'mp_weapon_sniper': (1, 0.0, 0.9152542372881358), 'mp_weapon_softball': (1, 0.0, 0.8644067796610164), 'mp_weapon_super_spectre': (1, 0.0, 0.8135593220338979), 'mp_weapon_thermite_grenade': (1, 0.0, 0.7627118644067794), 'mp_weapon_turretplasma': (1, 0.0, 0.7118644067796609), 'mp_weapon_vinson': (1, 0.0, 0.6610169491525424), 'mp_weapon_wingman': (1, 0.0, 0.6101694915254239), 'mp_weapon_wingman_n': (1, 0.0, 0.5593220338983045), 'mp_weapon_yh803_bullet': (1, 0.0, 0.5084745762711869), 'null': (1, 0.0, 0.45762711864406747), 'outOfBounds': (1, 0.0, 0.40677966101694985), 'phase_shift': (1, 0.0, 0.35593220338983045), 'pilot_emptyhanded': (1, 0.0, 0.30508474576271194), 'rodeo_battery_removal': (1, 0.0, 0.25423728813559343), 'spectre_melee': (1, 0.0, 0.20338983050847492), 'titan_execution': (1, 0.0, 0.15254237288135641), 'titan_explosion': (1, 0.0, 0.10169491525423702), 'titan_grapple': (1, 0.0, 0.05084745762711851), 'other': (1, 0.0, 0.0)}

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
    colors = []
    total = 0
    dict_weapon_with_kills = {}
    for i in response.keys():
        weaponstats = response[i]
        dict_weapon_with_kills[i] = weaponstats['kills']
        total += weaponstats['kills']

    handler = lambda p : response[p]['kills']
    result = sorted(dict_weapon_with_kills, key=handler, reverse=True)

    other = 0
    for j in result:
        if(dict_weapon_with_kills[j] > total/20):
            try:
                labels.append(weapon[j])
            except KeyError:
                labels.append(j)

            colors.append(weapon_color[j])
            values.append(dict_weapon_with_kills[j])
        else:
            other += dict_weapon_with_kills[j]

    labels.append("other")
    values.append(other)
    colors.append(weapon_color['other'])

    plt.style.use('ggplot')
    explode = [0.02] * len(values)
    patches, texts, pcts = plt.pie(x=values, autopct='%.0f%%', startangle=90, pctdistance=0.6, explode=explode, colors=colors, labels=labels,  wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
       textprops={'size': 'medium', })
    
    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
    plt.setp(pcts, color='white', fontweight='bold')
    plt.setp(texts, fontweight=600)
    
    plt.axis('equal')
    legend = plt.legend(labels=labels, loc='center', bbox_to_anchor=(0.5,-0.05,0,0), ncol=5, frameon=True)
    export_legend(legend)

    plt.savefig("Reuse/images/player_weapons_used.png", transparent=True)
    plt.close()

    img_file = discord.File("Reuse/images/player_weapons_used.png", filename="player_weapons_used.png")
    botmessage.set_image(url="attachment://player_weapons_used.png")

    return botmessage, img_file


def export_legend(legend, filename="Reuse/images/legend.png", expand=[-5,-5,5,5]):
    fig  = legend.figure
    fig.canvas.draw()
    bbox  = legend.get_window_extent()
    bbox = bbox.from_extents(*(bbox.extents + np.array(expand)))
    bbox = bbox.transformed(fig.dpi_scale_trans.inverted())
    fig.savefig(filename, dpi="figure", bbox_inches=bbox, transparent=True)


    # outer = plt.Circle(xy=(0,0), radius=1.02, facecolor='white')
    # plt.gca().add_artist(outer)