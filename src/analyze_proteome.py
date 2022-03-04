import pandas as pd


import seaborn as sns

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as mtick


colors_per_strain = {'Δ16':"#E69F00", 'MS56':"#56B4E9", 'MDS69':"#009E73",'MDS42':"#F0E442",'MDS12':"#0072B2",
                      'DGF298':"#D55E00", 'DGF327':"#CC79A7", 'MGF02':"#bdbdbd", 'MGF01':"#878500"}
markers_per_strain = {'Δ16':'--o', 'MS56':'--o', 'MDS69':'--o','MDS42':'--o','MDS12':'--o',
                      'DGF298':'--s', 'DGF327':'--s', 'MGF02':'--s', 'MGF01':'--s'}

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


def match_proteomic_data(names, cepas, proteomic_data):
    '''Gets the proteomic data from the given genes'''
    matched_genes_cepas={}
    for name in names:
        print(name)
        matched_genes_cepas[name]=proteomic_data[proteomic_data['Bnumber'].isin(cepas[name].Bnumber)].copy()
        gene_length  = cepas[name].set_index('Bnumber').loc[matched_genes_cepas[name].Bnumber,['Gen','Length']].values
        matched_genes_cepas[name].loc[:,['Gen NCBI', 'Length']] = gene_length

        # Reorganize columns
        first = list(matched_genes_cepas[name].columns[:2])
        second = list(matched_genes_cepas[name].columns[-2:])
        third = list(matched_genes_cepas[name].columns[2:-2])

        matched_genes_cepas[name] = matched_genes_cepas[name].loc[:,first+second+third]
    return(matched_genes_cepas)

def calculate_proteomic_load(names, matched_genes_cepas, proteome_size):
    '''Get the proteomic load of every condition and its percentage'''
    prot_load = []
    prot_perc = []

    for name in names:
        matched_genes = matched_genes_cepas[name]
        
        prot_load.append((matched_genes.sum()[4:26]).rename(name))
        prot_perc.append((matched_genes.sum()[4:26]/proteome_size.iloc[:,1:]*100).rename(index={0:name}))

    return(prot_load, prot_perc)






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



