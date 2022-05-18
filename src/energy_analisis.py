import numpy as np
import pandas as pd


def get_energy_consumption_production(me):
    atp_c = me.metabolites.get_by_id('atp_c')
    gtp_c = me.metabolites.get_by_id('gtp_c')
    muopt = me.solution.x[0]
    mu=muopt
    reactions_no_energy_production=[]
    reactions_energy_production={'Reactions':[],'Type':[],'ATP':[],'Used':[]}

    reactions_no_energy_production_consumption=[]
    reactions_energy_consumption={'Reactions':[],'Type':[],'ATP':[],'Used':[]}
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
            if gtp_c in reaction.products: 

                if "mu" in str(reaction.get_coefficient('gtp_c')):
                    gtp_value =eval(str(  (reaction.get_coefficient('gtp_c'))  )) 
                else:
                    gtp_value = reaction.get_coefficient('gtp_c')

                if reaction.metabolites[gtp_c]<0:
                    consume_gtp=True
                elif reaction.metabolites[gtp_c]>0:
                    produce_gtp = True
                    
    #       if reaction.x > 0:
    #          print(reaction.id,reaction.x)
    #       reactions_energy_production['Reactions']={"atp":atp_value,"gtp":gtp_value,"Total":atp_value+gtp_value,\
    #                                     "Usada":reaction.x*atp_value+gtp_value,"Tipo":type(reaction).__name__}
            if (produce_atp or produce_gtp) and reaction.x > 0:
                reactions_energy_production['Reactions'].append((reaction))
                reactions_energy_production['Type'].append((type(reaction).__name__))
                reactions_energy_production['Used'].append((reaction.x*(atp_value)))
                reactions_energy_production['ATP'].append((atp_value))
            elif (consume_atp) and reaction.x > 0:
                reactions_energy_consumption['Reactions'].append(str(reaction))
                reactions_energy_consumption['Type'].append((type(reaction).__name__))
                reactions_energy_consumption['Used'].append((reaction.x*(atp_value)))
                reactions_energy_consumption['ATP'].append((atp_value))
    return(reactions_energy_consumption,reactions_energy_production)

def energy_per_model(modelos, group=False):
    production_me = []
    consumption_me = {}
    consumption_me_group = {}
    consumption_perc = [] 

    for modelo in modelos:
        reactions_energy_consumption,reactions_energy_production = get_energy_consumption_production(modelos[modelo])
        #Production
        energy_production = pd.DataFrame.from_dict(reactions_energy_production).set_index('Reactions')
        production_me.append(energy_production.sum().Used)
        #Consumption
        energy_consumption = pd.DataFrame.from_dict(reactions_energy_consumption).set_index('Reactions')
        type_group_consumption = energy_consumption.Used.groupby(energy_consumption.Type)
        
        consumption_me_group['me'+modelo] = (abs(type_group_consumption.sum()))
        consumption_me['me'+modelo] = (abs(type_group_consumption.sum()).sum())
        
    if group:
        return(consumption_me, consumption_me_group, production_me)
    else:
        return(consumption_me, production_me)



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



def get_energy_ME_proteome(strains, genes_finales, proteomic_data, replication_cost, transcription_tcost, upf_cost ):
    costos_calclulados = { }
    for cepa in strains:
        T_replication_cost = 0
        T_transcription_gcost = 0
        T_transcription_tcost = 0
        T_upf_cost = 0

        for gen_info in genes_finales[cepa].iterrows():
            gen_name = gen_info[1].Bnumber 
            if gen_name is not np.nan: 
                largo_gen = gen_info[1].Length
                largo_gen = largo_gen/(1*10**6)
                if gen_name in list(proteomic_data.Bnumber):
                    fg_gen = proteomic_data[proteomic_data.Bnumber==gen_name].Glucosa
                    perc_gen = fg_gen *100/ proteomic_data.Glucosa.sum()
                    perc_gen = perc_gen.values[0]
                else:
                    perc_gen = 0
                T_replication_cost += replication_cost*largo_gen
        #             T_transcription_gcost += transcription_gcost*largo_gen
                T_transcription_tcost += transcription_tcost*largo_gen
                T_upf_cost += upf_cost*perc_gen
            else:
                continue
    #             print(gen)
        costos_calclulados[cepa] = {'Replication': T_replication_cost,
    #                                'transcription_g': T_transcription_gcost,
                                   'Transcription': T_transcription_tcost,
                                   'UPF': T_upf_cost,
                                   'Total': T_replication_cost + 
                                    T_transcription_tcost +
                                    T_upf_cost
                                   }
    return(costos_calclulados)