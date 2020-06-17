#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 09:46:09 2020

@author: elena
"""

import simuOpt
simuOpt.setOptions(alleleType='lineage', quiet=True)
import simuPOP as sim
import pandas as pd
import numpy as np
import seaborn as sns
import popmodel #contains all functions for simulation


# Pick a male bear
def bearFather(pop, subPop):
    all_males = [x for x in pop.individuals(subPop) if x.sex() == sim.MALE and x.age >= 3]
    iterator = 0
    while iterator < me:
        #print(len(all_males))
        for i in range(len(all_males)):
            all_males[i].mating +=1
            if all_males[i].age < 6:
                coeff =  success_repr_males
            else:
                coeff = success_dominant_males
            
            if (np.random.binomial(1, coeff) == 1) and (all_males[i].mating <= me):
                yield all_males[i]
            #print(all_males[i].mating)    
        iterator +=1

def bearMother(pop, subPop):
    all_females = [x for x in pop.individuals(subPop) if x.sex() == sim.FEMALE and x.hc == 0 and x.age >= 3]

    #print("bearMother: number of suitable females: {}".format(len(all_females)))

    while True:
        pick_female = np.random.randint(0, (len(all_females)))
        female = all_females[pick_female]
        female.hc = 1
        yield female

def simulation(me, iterations, generations, cro_to_slo, slo_to_cro, slo_cull, cro_cull):
    x = []  # empty list to store LD Ne calculations
    Ne = [] # empty list to store demographic Ne calculations
    
    for i in range(iterations):
        pop = sim.Population(size = [500, 500], loci=[1]*20,
                                 infoFields = ["age",'ind_id', 'father_idx', 'mother_idx', "mating", "hc",'migrate_to'],
                                 subPopNames = ["croatia", "slovenia"])
        sim.initInfo(pop = pop, values = list(map(int, np.random.negative_binomial(n = 1, p = 0.25, size=500))), infoFields="age")

        pop.setVirtualSplitter(sim.CombinedSplitter([
            sim.ProductSplitter([
                sim.SexSplitter(),
                sim.InfoSplitter(field = "age", cutoff = [1,3,6,15])])],
            vspMap = [[0,1], [2], [3], [4], [5,6,7,8], [9] ]))

        # Age groups: from 0 to 1 - cubs, from 1 to 3 - prereproductive, from 3 to 6 - reproductive class, from 6 to 15 - dominant
        pop.evolve(
            initOps=[
                sim.InitSex(),
                # random genotype
                sim.InitGenotype(freq=[0.01]*2 + [0.03]*2 + [0.23]*4),
                # assign an unique ID to everyone.
                sim.IdTagger(),
            ],
            # increase the age of everyone by 1 before mating.
            preOps=[sim.InfoExec('age += 1'),
                    sim.InfoExec('mating = 0'),
                    sim.PyOperator(func=popmodel.NaturalMortality),
                    sim.InfoExec("hc +=1 if 0 < hc < 3  else 0"), # Mother bear can't have cubs for two years after pregnancy
                    sim.Migrator(rate=[[cro_to_slo]],
                                 mode=sim.BY_PROPORTION,
                                 subPops=[(0, 0)],
                                 toSubPops=[1]), # reproductive males migrate from Cro to Slo
                    sim.Migrator(rate=[[slo_to_cro]],
                                 mode=sim.BY_PROPORTION,
                                 subPops=[(1, 0)],
                                 toSubPops=[0]),
                     sim.Stat(effectiveSize=sim.ALL_AVAIL, subPops=[(0,1),(0,2),(0,4), (1,1), (1,2), (1,4)], vars='Ne_demo_base'),
                     sim.Stat(effectiveSize=sim.ALL_AVAIL,subPops=[(0,1),(0,2),(0,4), (1,1), (1,2), (1,4)], vars='Ne_demo_base_sp')
                    #sim.PyEval(r'"Cro %d, Slo %d' ' % (Cro, Slo)', "Cro = pop.subPopSize(0)" "Slo = pop.subPopSize(1)",exposePop='pop'),
                    ],
            matingScheme=sim.HeteroMating([
                # CloneMating will keep individual sex and all
                # information fields (by default).
                # The age of offspring will be zero.

                sim.HomoMating(subPops=sim.ALL_AVAIL,
                    chooser=sim.CombinedParentsChooser(
                        fatherChooser=sim.PyParentsChooser(generator=bearFather),
                        motherChooser=sim.PyParentsChooser(generator=bearMother)
                    ),
                    generator=sim.OffspringGenerator(ops=[
                        sim.InfoExec("age = 0"),
                        sim.IdTagger(),
                        #sim.PedigreeTagger(),
                        sim.ParentsTagger(),
                        sim.MendelianGenoTransmitter()
                    ], numOffspring=(sim.UNIFORM_DISTRIBUTION, 1, 3))),
                sim.CloneMating(subPops=[(0,0), (0,1), (0,2), (0,4), (1,0), (1,1), (1,2), (1,4)], weight=-1),

            ], subPopSize=popmodel.demoModel),
            postOps = [
                sim.PyOperator(func=popmodel.cullCountry,param={"slo_cull": slo_cull, "cro_cull": cro_cull}),
                sim.PyOperator(func = popmodel.CalcNe, param={"me":me, "Ne":Ne}, begin=int(0.2*generations)),
                sim.PyOperator(func = popmodel.CalcLDNe, param={"me":me, "x":x}, begin=int(0.2*generations))
                       ],

            gen = generations
        )
    x = pd.concat(x)
    Ne = pd.concat(Ne)
    x.loc[x["population"] ==0,"population"] = "cro"
    x.loc[x["population"] ==1,"population"] = "slo"
    x = x[x['cutoff'] == 0]
    x = x.rename(columns={0: "Ne"})
    return x, Ne


#Baseline values
    
me = 2 # minimum value is 2!  mating events, how many times male bear can copulate 

#success_repr_males and success_dominant_males must be global variables, so it need to be set by the same name as here
success_repr_males = 1 # Chance of reproductive males to have an offspring (p in binomial distribution)
success_dominant_males = 1 # Chance of dominant males to have an offspring (p in binomial distribution)


iterations = 50 #number of iterations
generations = 50 # number of generations in each iteration

## Migration proportions
cro_to_slo = 0 #proportion of reproductive males, migrating from Croatia to Slovenia
slo_to_cro = 0 # and from Slovenia to Croatia.

## Proportion of animals in each age category to be culled
##(females, prereproductive, reproductive, dominant males)
slo_cull = {"f" : 0.1, "prerep": 0.1, "rep" : 0.1, "dom": 0.1}
cro_cull = {"f" : 0.1, "prerep": 0.1, "rep" : 0.1, "dom": 0.1}



#The function returns two dataframes: the first is Ne LD and the second is Ne demographic (EXACTLY THIS ORDER).
Ne_LD_baseline, Ne_demo_baseline = simulation(me, iterations, generations, cro_to_slo, slo_to_cro, slo_cull, cro_cull)

#Plot demographic (direct) effecitve population size dynamics
sns.relplot(x="gen", y="Ne", col = "me", hue="population", kind="line", data=Ne_demo_baseline)

#Plot linkage disequilibrium effecitve population size dynamics
sns.relplot(x="gen", y="Ne", col = "me", hue="population", kind="line", data=Ne_LD_baseline)





