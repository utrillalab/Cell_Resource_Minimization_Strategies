import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


colors = ["#FAB611",
"#6986C3",
"#81B540",
"#CC1330",
"#7760A7",]

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
    
    
def plot_type_energy(energy_consumption, energy_production):
    type_group_consumption = energy_consumption.Used.groupby(energy_consumption.Type)
    type_group_production=energy_production.Used.groupby(energy_production.Type)
    energia_producida = float(type_group_production.sum().values)
    no_usada = energia_producida + type_group_consumption.sum().sum()
    nueva_info=type_group_consumption.sum().append(pd.Series([no_usada], index=['Other']))
    nueva_info=abs(nueva_info)


    labels =list(nueva_info.index)
    sizes = list(abs(nueva_info.values))
    #colors
    colors = ['#CC1330','#6986C3','#FAB611','#7760A7','#6986C3','#6986C3','#81B540']
    explode = (0.05,0.05,0.05,0.05,0.05,0.05,0.05,)

    fig1, ax1 = plt.subplots()

    ax1.pie(sizes, colors = colors, labels=labels, autopct='%0.01f%%',
            startangle=90, pctdistance=0.5, explode = explode)

    #draw circle
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')  
    plt.tight_layout()
    plt.show()

    
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
    
    
    
def plot_glc_ox_atp(consumption_me, modelos, tipo):
    ''' Gráfica de consumo de energía con los ejes de consumo de glucosa y oxígeno'''
    
    if tipo=='Replication':
        title = "Increase of DNA Percentage in Cell"
    elif tipo == 'Transcription':
        title = "Increase of Transcribed Genes"
    elif tipo == 'UPF':
        title = "UPF"
        
    valores_metabolicos = pd.DataFrame({key:modelos[key].get_metabolic_flux() for key in modelos.keys()})
    glucosa = valores_metabolicos.loc['EX_glc__D_e'].sort_index()*(-1)
    oxigeno = valores_metabolicos.loc['EX_o2_e'].sort_index()*(-1)
    nombres= [nombre.split('me')[1] for nombre in consumption_me.keys()]
    x =  [float(nombre) for nombre in nombres]
    sns.set()
    sns.set_style("ticks")

    fig, ax1 = plt.subplots()

    color = '#CC1330'
    ax1.set_xlabel(title, fontsize=16, fontweight='bold')
    ax1.set_ylabel('ATP Consumption\n $mmol•gDW^{-1}•h^{-1}$', color=color,\
                  fontsize=16,fontweight='bold')

    lb1 = ax1.plot(*zip(*sorted(consumption_me.items())), color=color,marker='o',markersize=8, label = 'ATP')
    ax1.tick_params(axis='x', labelsize=14)
    ax1.tick_params(axis='y', labelcolor=color,labelsize=14)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = '#6986C3'
    ax2.set_ylabel('Oxygen and Glucose\nConsumption\n $mmol•gDW^{-1}•h^{-1}$', color='black',\
                  fontsize=16,fontweight='bold')  # we already handled the x-label with ax1

    lb2 = ax2.plot(*zip(*glucosa.sort_index().items()), color=color,marker='o',markersize=8, label = 'Glucose')
    color='#81B540'
    lb3 = ax2.plot(*zip(*oxigeno.sort_index().items()), color=color,marker='o',markersize=8, label = 'Oxygen')

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
    
    
def plot_energy_ME_proteome(names, aportaciones, leyendas, medio, colores=colors,  normalizado=False, eng= True, save=False, identifier=''):
    fig, ax = plt.subplots(figsize=(10,4))
    total_energia_producida = 68.89022155075351

    labelsize =16
    N = len(names)

    ind = np.arange(N)    # the x locations for the groups
    if N==4:
        width = 0.45       # the width of the bars: can also be len(x) sequence
    elif N==5:
        width = 0.5
    elif N==9:
        width = 0.75
    if normalizado:
        UPF_val = aportaciones.T.loc[names,'UPF']*100/aportaciones.T.loc[names,'Total']
        Trans_val = aportaciones.T.loc[names,'Transcription']*100/aportaciones.T.loc[names,'Total']
        Repli_val = aportaciones.T.loc[names,'Replication']*100/aportaciones.T.loc[names,'Total']
        
    else: 
        UPF_val = aportaciones.T.loc[names,'UPF']
        Trans_val = aportaciones.T.loc[names,'Transcription']
        Repli_val = aportaciones.T.loc[names,'Replication']
        
    p1 = ax.bar(ind*1.2, UPF_val, width, linewidth=0, color=colores[1])
    p2 = ax.bar(ind*1.2, Trans_val, width, linewidth=0,
                bottom=UPF_val, color=colores[0])
    p3 = ax.bar(ind*1.2, Repli_val, width, linewidth=0,
                 bottom=[sum(x) for x in zip(UPF_val,Trans_val)], color=colores[3])

    if normalizado:
        if eng:
            plt.ylabel('Percentage', fontsize=labelsize-2)
            normal = ' Normalized'

    elif normalizado ==False:
        if eng:
            ax.tick_params( labelsize=labelsize-4)
            ax.set_ylabel('Released ATP\n$mmol•gDW^{-1}•h^{-1}$', fontsize=labelsize-2)
            normal = ''
            
            ax2 = ax.twinx()
            ax2.set_ylim( (ax.get_ylim()[0]*100/total_energia_producida,
                        ax.get_ylim()[1]*100/total_energia_producida))
            
            ax2.tick_params( labelsize=labelsize-4)
    
    if eng:
        plt.title('Released Energy'+normal+" ("+medio+")", fontweight='bold' ,fontsize=labelsize)


    if normalizado == True:      
        add_line_MG(ax, -.1, 0.05)
        add_line_W3(ax, -.1, 0.57)
        ax.text((0.05+.48)/2, -0.17, 'MG1655', transform=ax.transAxes, fontsize=12) 
        ax.text((0.57)*1.28, -0.17, 'W3110', transform=ax.transAxes, fontsize=12) 
        xtick_labelsize = labelsize-4
    else:
        add_line_MG(ax2, -.1, 0.05)
        add_line_W3(ax2, -.1, 0.57)
        ax2.text((0.05+.48)/2, -0.17, 'MG1655', transform=ax2.transAxes, fontsize=12) 
        ax2.text((0.57)*1.28, -0.17, 'W3110', transform=ax2.transAxes, fontsize=12) 
        xtick_labelsize = labelsize-2
    
    
    plt.xticks(ind*1.2, tuple(names), fontsize= xtick_labelsize)
    plt.yticks(fontsize=xtick_labelsize)
    plt.legend((p1[0], p2[0], p3[0]), tuple(leyendas), bbox_to_anchor=(1.3, 1))
    if normalizado ==True:
        plt.gca().set_yticklabels(['{:.0f}%'.format(x) for x in plt.gca().get_yticks()]) 
        
    #print(ax.get_ylim(), ax2.get_ylim())
    plt.gca().set_yticklabels(['{:.1f}%'.format((x)) for x in plt.gca().get_yticks()]) 

    if save:
        plt.savefig("./"+identifier+"Released_Energy.pdf", dpi=600, format='pdf', bbox_inches='tight')
    plt.show()