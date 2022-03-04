import pandas as pd

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