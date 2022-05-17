import numpy as np

def get_energy_consumption_production(me):
    atp_c = me.metabolites.get_by_id('atp_c')
    gtp_c = me.metabolites.get_by_id('gtp_c')
    muopt = me.solution.x[0]
    mu=muopt
    reactions_no_energy_production=[]
    reactions_energy_production={'Reactions':[],'Type':[],'Total':[],'Used':[],'ATP':[]}

    reactions_no_energy_production_consumption=[]
    reactions_energy_consumption={'Reactions':[],'Type':[],'Total':[],'Used':[],'ATP':[]}
    for reaction in  me.reactions:

        if atp_c not in reaction.metabolites and gtp_c not in reaction.metabolites:
            reactions_no_energy_production.append(reaction)
        else:
            consume_atp=False
            produce_atp=False
            consume_gtp = False
            produce_gtp = False
            atp_value=0
            if atp_c in reaction.metabolites:

    #          break
                if "mu" in str(reaction.get_coefficient('atp_c')):
                    atp_value =eval(str(  (reaction.get_coefficient('atp_c'))  )) 
                else:
                    atp_value = reaction.get_coefficient('atp_c')
                if atp_value<0:
                    consume_atp=True
                elif atp_value>0:
                    produce_atp = True

    #       if reaction.x > 0:
    #          print(reaction.id,reaction.x)
    #       reactions_energy_production['Reactions']={"atp":atp_value,"gtp":gtp_value,"Total":atp_value+gtp_value,\
    #                                     "Usada":reaction.x*atp_value+gtp_value,"Tipo":type(reaction).__name__}
            if (produce_atp) and reaction.x > 0:
                reactions_energy_production['Reactions'].append((reaction))
                reactions_energy_production['Type'].append((type(reaction).__name__))
                reactions_energy_production['Total'].append((atp_value))
                reactions_energy_production['Used'].append((reaction.x*(atp_value)))
                reactions_energy_production['ATP'].append((atp_value))
            elif (consume_atp) and reaction.x > 0:
                reactions_energy_consumption['Reactions'].append(str(reaction))
                reactions_energy_consumption['Type'].append((type(reaction).__name__))
                reactions_energy_consumption['Total'].append((atp_value))
                reactions_energy_consumption['Used'].append((reaction.x*(atp_value)))
                reactions_energy_consumption['ATP'].append((atp_value))
    return(reactions_energy_consumption,reactions_energy_production)

def get_energy_per_gene(energy_consumption, me):
    
    # Metabolic reactions
    
    elegidos = energy_consumption[energy_consumption.Type=='MetabolicReaction']
    genes_met={}
    faltante_metabolico=0
    elegidos_maximos={}
    genes_tot=[]
    reactant_tipos=[]
    Complejos = []
    complex_formation = []

    for reaction in elegidos.index:
        elegidos_maximos[reaction]=[]
        a =me.reactions.get_by_id(reaction)

        for reactant in a.reactants:
            reactant_tipos.append(type(reactant).__name__)
            if((type(reactant).__name__)) =='Complex':
                Complejos.append(reactant)

                for reaccion_complejo in reactant.reactions:
                    if (type(reaccion_complejo).__name__) == 'ComplexFormation':
                        complex_formation.append(reaccion_complejo)

                        n_genes=0
                        for reactant_complejo in reaccion_complejo.reactants:
                            # Chech how many genes are involved
                            if (type(reactant_complejo).__name__) == 'TranslatedGene':
                                elegidos_maximos[reaction].append(reactant_complejo.id.split('_')[1])
                                genes_tot.append(reactant_complejo.id.split('_')[1])
                                n_genes+=1

                        # Check each gene contribution 
                        if n_genes > 1:
                            total = 0
                            valores = {}
                            for reactant_complejo in reaccion_complejo.reactants:
                                if (type(reactant_complejo).__name__) == 'TranslatedGene':
                                                        valores[reactant_complejo.id] = abs(reaccion_complejo.get_coefficient(reactant_complejo))
                            total = np.sum(list(valores.values()))

                            for key,value in valores.items():
                                bnumber_m= key.split('_')[1]
                                genes_met[bnumber_m] = genes_met.get(bnumber_m, 0) + value/total*a.x

                        elif n_genes == 1:
                            genes_met[bnumber_m] = genes_met.get(bnumber_m, 0) + a.x
                        else:
                            faltante_metabolico+=(a.x)

    # Transcription reaction
    
    transcription = energy_consumption.Used[energy_consumption.Type=="TranscriptionReaction"]
    genes_transcription={}
    for ind in transcription.index:

        rxn = me.reactions.get_by_id(ind)
        num_gen= 0
        lista_genes = []
        for gene in rxn.products:

            if type(gene).__name__ == 'TranscribedGene':
                lista_genes.append(gene.id)
        if len(lista_genes) > 1:
                        total = 0
                        valores = {}
                        for gene in lista_genes:
                               valores[gene] = abs(rxn.get_coefficient(gene))

                        total = np.sum(list(valores.values()))

                        for key,value in valores.items():
                            bnumber_m= key.split('_')[1]
                            genes_transcription[bnumber_m] = genes_transcription.get(bnumber_m, 0) + value/total*rxn.x
        elif len(lista_genes) == 1:
                            bnumber_m= lista_genes[0].split('_')[1]
                            genes_transcription[bnumber_m] = genes_transcription.get(bnumber_m, 0) + rxn.x
        else:
            print(rxn.x)
            
    # Translation 
    
    elegidos_trad = energy_consumption.loc[energy_consumption.Type=='TranslationReaction']
    elegidos_trad = elegidos_trad.Used
    
    # Sum all
    
    totales = {}
    for trans_bnumber in elegidos_trad.index:
        bnumber = trans_bnumber.split('_')[1]
        totales[bnumber] = genes_met.get(bnumber, 0) + elegidos_trad.loc[trans_bnumber] + genes_transcription.get(bnumber, 0)
        
    return(totales)