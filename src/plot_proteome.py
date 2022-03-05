import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mtick
import matplotlib.lines as mlines
import matplotlib as mpl


#mpl.rcParams['figure.dpi'] = 100


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
    plot_data=prot_load

        
    if conditions:
        plot_data = plot_data.loc[conditions, :]
    if strains:
        plot_data = plot_data.loc[:, strains]
        
    colors = []
    markers = []
    for strain in plot_data.columns:
        colors.append(mcolors.to_rgb(colors_per_strain[strain]))
        markers.append(markers_per_strain[strain])
        
    english = []
    for condition in plot_data.index:
        english.append(translate[condition])
    plot_data.plot(rot=90, linewidth=0, color=colors, ms=10, style=markers)
    
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
    
    plot_data = prot_perc
    if conditions:
        plot_data = plot_data.loc[conditions, :]
    if strains:
        plot_data = plot_data.loc[:, strains]
        
    a = plot_data.plot(rot=90,linewidth=0, color=colors, style=markers, ms=10)
    
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

    

def plot_strain_distribution(info_cepas, distribucion_prot, names, title, tipo, save=False, identifier=''):
    columna = tipo
    x_label= -0.8
    
    colores = []
    for strain in names:
        colores.append(mcolors.to_rgb(colors_per_strain[strain]))
        
    fig, axes = plt.subplots(1, 2, figsize=(8,3), dpi=100, sharex=True, sharey=True) #share y y share x
    
    for n,ax in enumerate(axes):
        
        if n==0:
            encimadas = [0, 1, 2]
        if n==1:
            encimadas = [2, 3]
        prom_f = []
        
        for m in encimadas:
                x_plot =  distribucion_prot.loc[distribucion_prot.Gen.isin(list(info_cepas[names[n+m]].values)), columna]
                x_plot = np.log10(x_plot)
                N, bins, patches = ax.hist(x_plot, alpha=1, bins=15,
                                           stacked=True, color=colores[n+m],
                                           linewidth=0.2,label=names[n+m],
                                           ec='white')
                
                
                suma_restante = 0
                
                for i, rect in enumerate(ax.patches[( 15 * (m-(n*2)) ):(15* (m+1-(n*2)) )]):
                    height = rect.get_height()
                    x_ax = rect.get_x()
                    if x_ax >= np.log10(0.1):
                        a=0
                    else:
                        suma_restante+=int(height) 
                prom_f.append(suma_restante*100/len(x_plot)) 
                
                
        red_line = mlines.Line2D([], [], color='#b80058', ls='--', label= '0.1 fg')
        handles = [red_line]
        labels = [h.get_label() for h in handles] 
        extra = plt.legend(handles=handles, labels=labels, bbox_to_anchor=(x_label, -0.12), fontsize=8)  
        plt.gca().add_artist(extra)
        
        if n == 0:
            ax.set_ylabel('Gene\nFrequency',fontsize=10)
            ax.set_title('MG1655', fontsize=10)
            ax.legend(bbox_to_anchor=(2.63, 1))

        if n==1 and len(names)==5:
            ax.set_xlabel('$log_{10}$(fg)',fontsize=10)
            ax.set_title('W3110', fontsize=10)
            ax.legend(bbox_to_anchor=(1, 0.65))

        ax.xaxis.set_tick_params(labelsize=8)
        ax.yaxis.set_tick_params(labelsize=8)

        mayores = 100-np.mean(prom_f)
        ax.annotate(f'{round(np.mean(prom_f),1)}%', xy=(-5, 40), 
                            xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',fontsize=7.5)

        ax.annotate(f'{round((mayores),1)}%', color='#b80058',
                    xy=(-0.2, 40), xytext=(0, 5), textcoords='offset points', ha='center', va='bottom',fontsize=7.5) 
        ax.axvline(np.log10(0.1), color='#b80058',ls='--')

        
        
    plt.suptitle('Proteome Distribution in '+title+" Strains ("+translate[tipo]+")",y=1.05,size=12, fontweight='bold')    

    if save:
        plt.savefig("./"+identifier+"FProteome_Strain_Distribution.pdf", dpi=600, format='pdf', bbox_inches='tight')

    