import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


colors = ["#FFB700",
"#648FFF",
"#82B541",
"#CC002D",
"#9B5EF0",]

new_colors = list(map(lambda x: mcolors.to_rgb(x), colors))
colors=new_colors


def add_line_MG(ax, xpos, ypos):
    line = plt.Line2D([ypos, ypos+ .48], [xpos, xpos], color='black', transform=ax.transAxes)
    line.set_clip_on(False)
    ax.add_line(line)

def add_line_W3(ax, xpos, ypos):
    line = plt.Line2D([ypos, ypos+ .39], [xpos, xpos], color='black', transform=ax.transAxes)
    line.set_clip_on(False)
    ax.add_line(line)
    
def plot_ME_energy(names, consumo, consumo_per):
    
    fig, ax1 = plt.subplots(figsize=(10,4))

    valores=[]
    for n in names:
        valores.append(consumo[n].Energy)
    valores_p=[]
    for n in names:
        valores_p.append(consumo_per[n].Energy)


    labelsize =16
    N = len(names[0:5])

    ind = np.arange(N)    # the x locations for the groups
    if N==4:
        width = 0.45       # the width of the bars: can also be len(x) sequence
    elif N==5:
        width = 0.8
    elif N==9:
        width = 0.75


    lb1 = ax1.bar(ind*1.2, valores[0:5], width, color=colors[0:5], tick_label=names[0:5])
    ax1.tick_params( labelsize=labelsize-4)
    ax1.set_ylabel('Released ATP\n$mmol•gDW^{-1}•h^{-1}$', fontsize=labelsize-2)

    ax2 = ax1.twinx()
    ax2.bar(ind*1.2, valores_p[0:5], width, color=colors[0:5], tick_label=names[0:5])
    ax2.tick_params(labelsize=labelsize-4)

    add_line_MG(ax2, -.1, 0.05)
    add_line_W3(ax2, -.1, 0.57)

    ax2.text((0.05+.48)/2, -0.17, 'MG1655', transform=ax2.transAxes, fontsize=12) 
    ax2.text((0.57)*1.28, -0.17, 'W3110', transform=ax2.transAxes, fontsize=12) 

    # plt.yticks(fontsize=labelsize-4)

    plt.title('ME Model Genes Related Released Energy',fontweight='bold' ,fontsize=labelsize)
    plt.gca().set_yticklabels(['{:.1f}%'.format((x)) for x in plt.gca().get_yticks()]) 
    plt.show()
    
    
    
def plot_glc_ox_atp(consumption_me,modelos):
    ''' Gráfica de consumo de energía con los ejes de consumo de glucosa y oxígeno'''
    
    valores_metabolicos = pd.DataFrame({key:modelos[key].get_metabolic_flux() for key in modelos.keys()})
    glucosa = valores_metabolicos.loc['EX_glc__D_e'].sort_index()*(-1)
    oxigeno = valores_metabolicos.loc['EX_o2_e'].sort_index()*(-1)
    nombres= [nombre.split('me')[1] for nombre in consumption_me.keys()]
    x =  [float(nombre) for nombre in nombres]
    sns.set()
    sns.set_style("ticks")

    fig, ax1 = plt.subplots()

    color = '#CC002D'
    ax1.set_xlabel('UPF',fontsize=16,fontweight='bold')
    ax1.set_ylabel('Consumo de ATP\n $mmol•gDW^{-1}•h^{-1}$', color=color,\
                  fontsize=16,fontweight='bold')

    lb1 = ax1.plot(*zip(*sorted(consumption_me.items())), color=color,marker='o',markersize=8, label = 'ATP')
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelcolor=color,labelsize=14)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = '#648FFF'
    ax2.set_ylabel('Consumo de\noxígeno y glucosa\n $mmol•gDW^{-1}•h^{-1}$', color='black',\
                  fontsize=16,fontweight='bold')  # we already handled the x-label with ax1

    lb2 = ax2.plot(*zip(*glucosa.sort_index().items()), color=color,marker='o',markersize=8, label = 'Glucosa')
    color='#82B541'
    lb3 = ax2.plot(*zip(*oxigeno.sort_index().items()), color=color,marker='o',markersize=8, label = 'Oxígeno')

    ax2.tick_params(axis='y', labelcolor='black')

    # fig.tight_layout()  
    a = plt.xticks()[0]
    plt.xticks(a, [str(nombre) for nombre in sorted(x)])
#     plt.xticks(a, ['0.24','0.27','0.30','0.33','0.36'])
    plt.yticks(fontsize=14)

    leg = lb1 + lb2 + lb3
    labs = [l.get_label() for l in leg]
    ax1.legend(leg, labs,loc='center left', bbox_to_anchor=(1.25, 0.5))
    plt.show()