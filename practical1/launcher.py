import os, logging, time
from variation import CrossoverType, Variation
from simple_genetic_algorithm import SimpleGeneticAlgorithm
from fitness_function import FitnessFunction, OptimumFoundCustomException
from itertools import product as cp

population_sizes = range(20, 200+1, 20)
ms = [1, 2, 4, 8, 16]
ks = [5]
crossoverTypes = list(CrossoverType)

def main():
    generations_limit = -1
    evaluations_limit = -1
    time_limit = 3.0 # in seconds

    if 'experiments' not in os.listdir('.'):
        os.mkdir('experiments')

    # set up file outputs
    f = open("experiments/results.csv", "w+")
    f.write("crossover_type,population_size,m,k,d,optimal,generations,evaluations,time,best_fitness,isOptimal\n")

    i = -1
    for (ct, m, k, p, _) in cp(crossoverTypes, ms, ks, population_sizes, range(5)):
        # find the values for d to test
        for d in [1/k, 1-1/k]:
            # run genetic algorithm
            i += 1
            print("Starting run {run} with pop_size={p}, m={m}, k={k}, d={d}, crossover_type={ct}".format(
                  run=i, p=p, m=m, k=k, d=d, ct=ct.name
            ))
            sga = SimpleGeneticAlgorithm(p, m, k, d, ct)
            optimumFound = False
            try:
                sga.run(generations_limit, evaluations_limit, time_limit)
            except OptimumFoundCustomException:
                optimumFound = True

            print("""{outcome} {bf} found at
            generation\t{gen}
            evaluations\t{evals}
            time\t{time}
            elite\t{elite}
            """.format(outcome = "Optimum" if optimumFound == True else "Best Fitness",
                       bf = sga.fitness_function.elite.fitness,
                       gen = sga.generation,
                       evals = sga.fitness_function.evaluations,
                       time = time.time() - sga.start_time,
                       elite = sga.fitness_function.elite
            ))

            f.write("{ct},{p},{m},{k},{d},{optimal},{gen},{evals},{time},{bf},{found}\n".format(
                ct = ct.name, p=p, m=m, k=k, d=d, optimal=sga.fitness_function.optimum,
                gen = sga.generation, evals = sga.fitness_function.evaluations,
                time = time.time() - sga.start_time, bf = sga.fitness_function.elite.fitness,
                found = optimumFound
            ))


if __name__ == "__main__":
    main()
