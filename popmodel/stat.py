# -*- coding: utf-8 -*-
# Function to calculate Ne as described in (Waples, 2006) (the same as in Ne estimator v. 2 software)
import simuPOP as sim
import pandas as pd
from statistics import mean 

def CalcLDNe(pop, param):
    sim.stat(pop = pop, popSize = "subPopSize")
    sim.stat(pop= pop, effectiveSize=sim.ALL_AVAIL, vars="Ne_LD_sp") #calculate Ne for both populations separately
    #Write results to the dataframe
    for p in [0, 1]:
        a = pd.DataFrame.from_dict(pop.dvars(p).Ne_LD, orient="index")
        a["cutoff"] = a.index
        a["population"] = p #population 0 = Croatia, population 1 = Slovenia
        a["Size"] = pop.dvars().subPopSize[p] #Actual population size
        a["gen"] = pop.dvars().gen
        a["me"] = param["me"]
        param["x"].append(a)

    cro_size = pop.subPopSize(0)
    slo_size = pop.subPopSize(1)
    pop.mergeSubPops([0, 1]) # Merge subpopulations to calculate Ne
    sim.stat(pop=pop, effectiveSize=sim.ALL_AVAIL, vars="Ne_LD")
    pop.splitSubPop(0,[cro_size, slo_size])
    pop.setSubPopName('croatia', 0)
    pop.setSubPopName('slovenia', 1)
    a = pd.DataFrame.from_dict(pop.dvars().Ne_LD, orient="index")
    a["cutoff"] = a.index
    a["population"] = "all"
    a["Size"] = pop.popSize()
    a["gen"] = pop.dvars().gen
    a["me"] = param["me"]
    param["x"].append(a)
    print("Run generation", pop.dvars().gen)
    return True



def CalcdemoNe(pop):
    sim.InfoSplitter(field = "age", cutoff = [3,10])
    sim.stat(pop=pop, effectiveSize=range(2), subPops= [(0,1), (1,1)], vars='Ne_demo_base_sp')
    sim.stat(pop=pop, effectiveSize=range(2), subPops=[(0,1)], vars='Ne_demo_base')
    return True





#Demographic Ne here is basically  an effective number of breeders - it calculated for adults
    
def CalcNe(pop, param):
    sim.stat(pop=pop, effectiveSize=sim.ALL_AVAIL, subPops=[(0,1),(0,2),(0,4), (1,1), (1,2), (1,4)], vars='Ne_demo_sp')
    sim.stat(pop=pop, effectiveSize=sim.ALL_AVAIL, subPops=[(0,1),(0,2),(0,4), (1,1), (1,2), (1,4)], vars='Ne_demo')
    a = pd.DataFrame({"Ne":[pop.dvars((0,1)).Ne_demo[1] + pop.dvars((0,2)).Ne_demo[1] + pop.dvars((0,4)).Ne_demo[1],
                            pop.dvars((1,1)).Ne_demo[1] + pop.dvars((1,2)).Ne_demo[1] + pop.dvars((1,4)).Ne_demo[1],
                            mean(pop.dvars().Ne_demo.values())], 
                            "population":["cro", "slo", "all"]})  
    a["gen"] = pop.dvars().gen
    a["me"] = param["me"]
    param["Ne"].append(a)
    return True


def splitCalcMerge(pop, param):
    #pop_size = pop.popSize()
    sim.InfoSplitter(field = "age", cutoff = [1,8])
    sim.stat(pop = pop, popSize = "subPopSize")
    sim.stat(pop= pop, effectiveSize=sim.ALL_AVAIL, vars="Ne_LD", subPops=[(0,1)], suffix="_Cro")
    sim.stat(pop=pop, effectiveSize=sim.ALL_AVAIL, vars="Ne_LD", subPops=[(1,1)], suffix="_Slo")

    a = pd.DataFrame.from_dict(pop.dvars().Ne_LD_Cro, orient="index")
    a["cutoff"] = a.index
    a["population"] = 0
    a["Size"] = pop.dvars().subPopSize[0]
    a["gen"] = pop.dvars().gen
    param["x"].append(a)
    a = pd.DataFrame.from_dict(pop.dvars().Ne_LD_Slo, orient="index")
    a["cutoff"] = a.index
    a["population"] = 1
    a["Size"] = pop.dvars().subPopSize[1]
    a["gen"] = pop.dvars().gen
    param["x"].append(a)

    cro_size = pop.subPopSize(0)
    slo_size = pop.subPopSize(1)
    pop.mergeSubPops([0, 1])
    sim.InfoSplitter(field="age", cutoff=[1,8])
    sim.stat(pop=pop, effectiveSize=sim.ALL_AVAIL, vars="Ne_LD", subPops=[(0,1)])
    pop.splitSubPop(0,[cro_size, slo_size])
    pop.setSubPopName('croatia', 0)
    pop.setSubPopName('slovenia', 1)
    a = pd.DataFrame.from_dict(pop.dvars().Ne_LD, orient="index")
    a["cutoff"] = a.index
    a["population"] = "all"
    a["Size"] = pop.popSize()
    a["gen"] = pop.dvars().gen
    param["x"].append(a)
    return True