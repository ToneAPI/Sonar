import discord
from matplotlib import patheffects
import matplotlib.pyplot as plt
import numpy as np
import requests

def make_donut_chart(botmessage, labels, values, colors):
    plt.figure().clear()

    plt.style.use('ggplot')
    explode = [0.02] * len(values)
    patches, texts, pcts = plt.pie(x=values, autopct='%.0f%%', startangle=90, pctdistance=0.6, explode=explode, colors=colors, labels=labels,  wedgeprops={'linewidth': 1.0, 'edgecolor': 'white'},
       textprops={'size': 'medium','color': 'white'})

    for i, patch in enumerate(patches):
        texts[i].set_color(patch.get_facecolor())
        plt.setp(pcts, color='white', fontweight='bold')
        plt.setp(texts, fontweight=600)

    for pct in pcts:
        pct.set_color('white')
        pct.set_path_effects([patheffects.Stroke(linewidth=1, foreground='black'), patheffects.Normal()])

        
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
