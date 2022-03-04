import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mtick
import matplotlib.lines as mlines


colors_per_strain = {'Δ16':"#E69F00", 'MS56':"#56B4E9", 'MDS69':"#009E73",'MDS42':"#F0E442",'MDS12':"#0072B2",
                      'DGF298':"#D55E00", 'DGF327':"#CC79A7", 'MGF02':"#bdbdbd", 'MGF01':"#878500"}
markers_per_strain = {'Δ16':'--o', 'MS56':'--o', 'MDS69':'--o','MDS42':'--o','MDS12':'--o',
                      'DGF298':'--s', 'DGF327':'--s', 'MGF02':'--s', 'MGF01':'--s'}


colors_distribution = ["#E69F00", "#56B4E9"]
colors_distribution = [mcolors.to_rgb(color) for color in colors_distribution ]

english_cond = ["LB","Glycerol + AA","42°C Glucose","Fructose","pH6 Glucose",
               "Glucose","Osmotic-stress Glucose","Xylose","Chemostat µ=0.5",
               "Mannose","Glycerol","Glucosamine","Succinate","Fumarate","Pyruvate",
               "Quimiostato µ=0.35","Acetate","Galactose","Chemostat µ=0.20",
               "Chemostat µ=0.12","Stationary Phase 1 Day","Stationary Phase 3 Days"]
spanish_cond = ["LB","Glicerol + AA","42°C glucosa","Fructosa","pH6 glucosa",
             "Glucosa","Estrés-osmótico glucosa","Xilosa","Quimiostato µ=0.5",
             "Manosa","Glicerol","Glucosamina","Succinato","Fumarato","Piruvato",
             "Quimiostato µ=0.35","Acetato","Galactosa","Quimiostato µ=0.20",
             "Quimiostato µ=0.12","Fase estacionaria 1 día","Fase estacionaria 3 días"]

translate = dict(zip(spanish_cond, english_cond))




def plot_perc_load(prot_load, prot_perc, conditions=None, strains=None, save=False, identifier=''):
    labelsize = 16
#     ticksize=24
    sns.set()
    sns.set_style("white")
    sns.set_style("ticks")
    dd=(pd.concat(prot_load,axis=1))

        
    if conditions:
        dd = dd.loc[conditions, :]
    if strains:
        dd = dd.loc[:, strains]
        
    colors = []
    markers = []
    for strain in dd.columns:
        colors.append(mcolors.to_rgb(colors_per_strain[strain]))
        markers.append(markers_per_strain[strain])
        
    english = []
    for condition in dd.index:
        english.append(translate[condition])
    dd.plot(rot=90, linewidth=0,color=colors,ms=8,style=markers)
    
    condiciones = [n+' —          ' for n in english]
    ubicacion = range(0,len(condiciones))
    plt.xticks(ubicacion, condiciones,fontsize=labelsize-2)
    plt.title('Released Proteomic Load',fontsize=labelsize, fontweight="bold")

        
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
#     plt.xlabel('Condiciones')
    plt.ylabel('fg', fontsize=labelsize-2)
    left, right = plt.xlim()
    plt.suptitle('μ',y=0.05,size=labelsize-2, x=0.118)

    #plt.savefig("./Figuras/"+identifier+"Proteomic_Fentograms_Calculation.pdf", dpi=600, format='pdf', bbox_inches='tight')
    plt.show()
    
    dd = (pd.concat(prot_perc,axis=0).T)
    if conditions:
        dd = dd.loc[conditions, :]
    if strains:
        dd = dd.loc[:, strains]
        
    a = dd.plot(rot=90,linewidth=0, color=colors, style=markers, ms=8)
    
    condiciones = [n+' —          ' for n in english]
    ubicacion = range(0,len(condiciones))
    plt.xticks(ubicacion, condiciones,fontsize=labelsize-2)
    plt.title('Released Proteome Percentage',fontsize=labelsize, fontweight="bold")

        
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    a.yaxis.set_major_formatter(mtick.PercentFormatter(100.0))
    left, right = plt.xlim()
    plt.suptitle('μ',y=0.05,size=labelsize-2, x=0.118)
    
    
    #if save:
        #plt.savefig("./Figuras/"+identifier+"Proteomic_Percentaje_Calculation.pdf", dpi=600, format='pdf', bbox_inches='tight')
    plt.show()

def plot_distribution(distribucion_prot, tipo, eng=False, save =False, identifier=''):
    
    if tipo =='Promedio' or tipo == 'Average':
        columna = tipo
        if eng:
            titulo = "Average Proteome Distribution"
        else:
            titulo = "Distribución del promedio del proteoma"
    else:
        columna = tipo
        if eng:
            titulo = "Proteome Distribution ("+translate[tipo]+")"
        else:
            titulo = "Distribución del proteoma ("+tipo+")"
    label_size = 14
    n=0
    fig, ax = plt.subplots( dpi=100, sharex=False, sharey=False)
# for n,ax in enumerate(axes):
    x_plot =  distribucion_prot.loc[:,columna]
    x_plot =np.log10(x_plot)
    N, bins, patches = ax.hist(x_plot, alpha=1, bins=35, stacked=True, color=colors_distribution[n],linewidth=0.2)
    ax.set_title( titulo, fontsize=label_size, fontweight="bold")
#     ax.set_xlim(-.020, max(x_plot)); ax.set_ylim(0, len(x_plot)+len(x_plot)*0.1);
    ax.set_ylabel('Gene\nFrequency',fontsize=label_size-2)
    ax.set_xlabel('$log_{10}$(fg)',fontsize=label_size-2)
    ax.xaxis.set_tick_params(labelsize=label_size-4)
    ax.yaxis.set_tick_params(labelsize=label_size-4)
    
    suma_restante=0
    for i,rect in enumerate(ax.patches):
        height = rect.get_height()
        x_ax = rect.get_x()
        if x_ax >= np.log10(0.1):
            ax.annotate(f'{int(height)}', xy=(rect.get_x()+rect.get_width(), height), 
                        xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',fontsize=8) 
        else:
            suma_restante+=int(height)
            patches[i].set_facecolor(colors_distribution[n+1])
            
    
    suma_restante
    mayores = len(x_plot)-suma_restante
    ax.annotate(f'{suma_restante}\n'+f'{round(suma_restante*100/len(x_plot),1)}%', xy=(-2, 75), 
                        xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',fontsize=10)
    
    ax.annotate(f'{mayores}\n'+f'{round((mayores)*100/len(x_plot),1)}%',
                xy=(-0.5, 25), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',fontsize=10) 
    ax.axvline(np.log10(0.1), color='#b80058',ls='--')
    
    blue_line = mlines.Line2D([], [], color=colors_distribution[n+1], markersize=10, ls='', marker='s', label='< 0.1 fg')
    green_line = mlines.Line2D([], [], color=colors_distribution[n], markersize=10, ls='', marker='s',label='> 0.1 fg')

    handles = [blue_line,green_line]
    labels = [h.get_label() for h in handles] 
    
    plt.legend(handles=handles, labels=labels, loc='best', fontsize=10)  
#     plt.tight_layout()
    if save:
        plt.savefig("./Figuras/"+identifier+"Proteome_Distribution.pdf", dpi=600, format='pdf', bbox_inches='tight')

    plt.show()
