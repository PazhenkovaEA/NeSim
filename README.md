# NeSim

The simulations performed to show an impact of some factors on the key metrics used in ecology and conservation study - effective population size.
Here we demonstrated, how migrations, different management strategies and features of mating biology can have an influence on effective population size (calculated with LD method according to Waples, 2006)) and effective number of breeders in populations with overlapping generations.
Model species is brown bear, *Ursus arctos*, and modelled processes reflect long-termed observations of bear biology in Croatia and Slovenia. One of the key parameters in this simulations is different hunting management strategy. In Croatian population mostly old males are taken from population, and in Slovenia implements the take of younger individuals.

Simulations are performed using simuPOP package. 

## Scheme of the simulaitons 
### Baseline parameters

iterations = 50 # Number of iterations
generations = 50 # Number of generations in each iteration
* Mating parameters
me = 2   # Number of mating events, defines maximum times male bear can copulate.
success_repr_males = 1 # Chance of reproductive males to have an offspring (p in binomial distribution)
success_dominant_males = 1 # Chance of dominant males to have an offspring (p in binomial distribution)

* Migration proportions
cro_to_slo = 0 #proportion of reproductive males migrate from Croatia to Slovenia
slo_to_cro = 0 # and from Slovenia to Croatia.

* Proportion of animals in each age category to be culled 
(females, prereproductive, reproductive, dominant males)
slo_cull = {"f" : 0.1, "prerep": 0.1, "rep" : 0.1, "dom": 0.1}
cro_cull = {"f" : 0.1, "prerep": 0.1, "rep" : 0.1, "dom": 0.1}

### Population features
2 subopopulations are generated with equal sex proportion. Age varies from 0 to 15, animals older than 15 removed from the population. 
Males in the population divided on following age categories:

* Cubs - from 0 to 1 y.o.;
* Prereproductive - from 1 to 3 y.o.;
* Reproductive - from 3 to 6;
* Dominant - from 6 to 15 y.o.

We modelled 20 neutral unlinked microsattelite-like loci, when each locus has 6 possible alleles. Genotypes have equal frequencies in the beginning. 

### Reproduction and demographic schemes

Father randomly picked up from reproductive and dominant males. Each bear can participate in reproduction maximum **me** times with probability of success **success_repr_males** or **success_dominant_males**. 
Females become reproductive at 3 years. Female can’t have cubs during 2 years after mating. 
Number of offspring calculates with demoModel function as number of reproductive females multiplied on 1.9 (average number of offspring).

### Mortality
3% of natural mortality (take 3% of random individuals). Natural mortality applied before mating.
Hunting mortality is a proportion of randomly taken animals, defined separately for females, prereproductive, reproductive and dominant males.
Cubs and females with cubs cannot be culled. Hunting applied after mating.

### Statistics

burn-in = 20% of number of generations. 

Effective population size was calculated using LD method as described
(Waples, 2006). Each generation Ne was estimated for each subpopulation
separately and for merged total population.
Rare alleles can have a significant influence on the result (since they can
lead to inflated measure of LD), so simuPOP provides estimates that ignores alleles with
frequencies less than 0 (all alleles are kept), 0.01, 0.02 and 0.05. Since we didn’t define
any rare alleles, we didn’t use a threshold.

True (demographic) effecitve population size here is a basically an effective number of breeders (http://simupop.sourceforge.net/manual_release/build/userGuide_ch5_sec11.html#effective-population-size). It counts how many alleles each parent has contributed to the offspring generation, and calculate demographic effective size accordingly. Both statistics are calculated for two subpopulations separately and for entire population (assuming panmixy).

### Explanation of infoFields
* "age": age of individual (in years), changes in range \[0:15]
* 'ind_id':tracks individuals
* 'father_idx' and 'mother_idx': tracks parents
* "mating": tracks how many times male participated in reproduction per generation, changes in range \[0:me]
* "hc": counts for how many years females stayed with a cub. Changes in range \[0:2]
* 'migrate_to': define direction of migraion


