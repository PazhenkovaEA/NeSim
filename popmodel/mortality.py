import random as random

def cullCountry(pop, param):

   slo_f = [x for x in pop.individuals([1, 4]) if x.hc == 0]
   sampling_f = random.choices(slo_f, k=int(param["slo_cull"]["f"]*len(slo_f)))
   out_f_ids = [x.ind_id for x in sampling_f]
   pop.removeIndividuals(IDs=out_f_ids, idField="ind_id")

   cro_f = [x for x in pop.individuals([0, 4]) if x.hc == 0]
   sampling_f = random.choices(cro_f, k=int(param["cro_cull"]["f"]*len(cro_f)))
   out_f_ids = [x.ind_id for x in sampling_f]
   pop.removeIndividuals(IDs=out_f_ids, idField="ind_id")

   slo_prerep = [x for x in pop.individuals([1, 0]) if x.age != 0]
   sampling_prerep = random.choices(slo_prerep, k=int(param["slo_cull"]["prerep"]*len(slo_prerep)))
   out_prerep_ids = [x.ind_id for x in sampling_prerep]
   pop.removeIndividuals(IDs=out_prerep_ids, idField="ind_id")

   cro_prerep = [x for x in pop.individuals([0, 0]) if x.age != 0]
   sampling_prerep = random.choices(cro_prerep, k=int(param["cro_cull"]["prerep"]*len(cro_prerep)))
   out_prerep_ids = [x.ind_id for x in sampling_prerep]
   pop.removeIndividuals(IDs=out_prerep_ids, idField="ind_id")


   slo_rep = [x for x in pop.individuals([1, 1])]
   sampling_rep = random.choices(slo_rep, k=int(param["slo_cull"]["rep"]*len(slo_rep)))
   out_rep_ids = [x.ind_id for x in sampling_rep]
   pop.removeIndividuals(IDs=out_rep_ids, idField="ind_id")

   cro_rep = [x for x in pop.individuals([0, 1])]
   sampling_rep = random.choices(cro_rep, k=int(param["cro_cull"]["rep"]*len(cro_rep)))
   out_rep_ids = [x.ind_id for x in sampling_rep]
   pop.removeIndividuals(IDs=out_rep_ids, idField="ind_id")

   slo_postrep = [x for x in pop.individuals([1, 2])]
   sampling_postrep = random.choices(slo_postrep, k=int(param["slo_cull"]["dom"]*len(slo_postrep)))
   out_postrep_ids = [x.ind_id for x in sampling_postrep]
   pop.removeIndividuals(IDs=out_postrep_ids, idField="ind_id")

   cro_postrep = [x for x in pop.individuals([0, 2])]
   sampling_postrep = random.choices(cro_postrep, k=int(param["cro_cull"]["dom"]*len(cro_postrep)))
   out_postrep_ids = [x.ind_id for x in sampling_postrep]
   pop.removeIndividuals(IDs=out_postrep_ids, idField="ind_id")
   #print(pop.subPopSize(0))
   #print(pop.subPopSize(1))

   return True



def NaturalMortality(pop):
    all_inds = [x for x in pop.individuals()]
    sampling_m = random.choices(all_inds, k=int(0.02 * len(all_inds)))
    out_ids = [x.ind_id for x in sampling_m]
    pop.removeIndividuals(IDs=out_ids, idField="ind_id")
    return True
