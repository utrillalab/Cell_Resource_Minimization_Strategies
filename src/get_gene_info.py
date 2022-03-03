from Bio import SeqIO
import pandas as pd

def get_genome_info(genome_path):
    genome_gb = next(SeqIO.parse(genome_path, "genbank"))
    datos={'Gen':[],
          'Bnumber':[],
          'Start':[],
          'End':[]}
    
    if 'MG1655' in genome_path:

        for i,feature in enumerate(genome_gb.features):
            if feature.type == 'gene':
                datos['Gen'].append(feature.qualifiers['gene'][0])
                datos['Bnumber'].append(feature.qualifiers['locus_tag'][0])
                datos['Start'].append(feature.location.nofuzzy_start)
                datos['End'].append(feature.location.nofuzzy_end)
    elif 'W3110' in genome_path:
        take=False
        for i,feature in enumerate(genome_gb.features):
            if feature.type == 'gene':
                take=True
                name=feature.qualifiers['gene'][0]
                continue
            if take and feature.qualifiers['gene'][0] == name:
                datos['Gen'].append(feature.qualifiers['gene'][0])
                bnumber = feature.qualifiers['note'][0].rsplit(':',1)[-1]
                if ';' in bnumber:
                    bnumber = bnumber.split(';')[0]
                datos['Bnumber'].append(bnumber)
                datos['Start'].append(feature.location.nofuzzy_start)
                datos['End'].append(feature.location.nofuzzy_end)
                take=0
                name=None
        
    else:
        print('Genome not taken into account')

    genome = pd.DataFrame.from_dict(datos)
    genome.loc[:, 'Length'] = genome.loc[:, 'End'] - genome.loc[:,'Start'] +1
    
    return(genome)
    
def get_genes_from_ranges(rangos, genome):
    
    for column in rangos.columns:
        if '_R' in column:
            fin = column
        elif '_L' in column:
            inicio=column
    
    rangos[inicio] = rangos[inicio].astype(int)
    rangos[fin] = rangos[fin].astype(int)

    rangos_r = rangos.loc[rangos.index.repeat(len(genome))]
    rangos_r = rangos_r.reset_index()
    genome_r = genome
    
    for n in range(len(rangos)-1):
        genome_r = genome_r.append(genome)

    genome_r = genome_r.reset_index()    
    
    prim_caso = (rangos_r[inicio] > genome_r['Start'] ) & ( rangos_r[inicio] < genome_r['End'])
    seg_caso = (rangos_r[inicio] < genome_r['Start'] ) & ( rangos_r[fin] > genome_r['Start'])
    todo = prim_caso | seg_caso
    lista_genes_R = genome_r.loc[todo,['Bnumber', 'Gen', 'Length']]
    print(len(lista_genes_R))
    return(lista_genes_R)