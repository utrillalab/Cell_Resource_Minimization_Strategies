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

    #             break
                if "mu" in str(reaction.get_coefficient('atp_c')):
                    atp_value =eval(str(  (reaction.get_coefficient('atp_c'))  )) 
                else:
                    atp_value = reaction.get_coefficient('atp_c')
                if atp_value<0:
                    consume_atp=True
                elif atp_value>0:
                    produce_atp = True

    #         if reaction.x > 0:
    #             print(reaction.id,reaction.x)
    #         reactions_energy_production['Reactions']={"atp":atp_value,"gtp":gtp_value,"Total":atp_value+gtp_value,\
    #                                                 "Usada":reaction.x*atp_value+gtp_value,"Tipo":type(reaction).__name__}
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