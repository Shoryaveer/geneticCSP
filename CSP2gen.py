from random import choices, choice, random, seed
# from typing import Literal

'''
TODO:
- make proper docs
- make testing suite
'''


class BadGeneLength(Exception):
    pass


class BadMutationChance(Exception):
    pass


class Cgen():

    def __init__(self) -> None:
        pass

    def _get_likelihood(self) -> list:
        retList = []
        for i in self._fit_scores:
            retList.append(i/sum(self._fit_scores))
        return retList

    def _sort_by_fitness(self) -> None:
        # TODO: improve this by implementing a better sort
        for i in range(len(self._fit_scores)-1):
            for j in range(len(self._fit_scores) - i - 1):
                if self._fit_scores[j] < self._fit_scores[j+1]:
                    self._fit_scores[j], self._fit_scores[j+1] = self._fit_scores[j+1], self._fit_scores[j]
                    self._population[j], self._population[j+1] = self._population[j+1], self._population[j]

    def _two_point_crossover(self) -> None:
        gene_len = len(self._population[0])
        for i in range(0, len(self._population), 2):
            if i + 1 < len(self._population):  # Ensure there's a pair to crossover

                if len(self._population[i]) != len(self._population[i+1]):
                    raise BadGeneLength('The population given does not have uniform member length.')

                # Generate two distinct points for crossover
                point1, point2 = sorted(
                    [choice(range(1, gene_len)), choice(range(1, gene_len))])

                # Ensure the two points are not the same for effective crossover
                while point1 == point2:
                    point1, point2 = sorted(
                        [choice(range(1, gene_len)), choice(range(1, gene_len))])

                    # Swap the genes between point1 and point2 for crossover
                    self._population[i][point1:point2], self._population[i+1][point1:point2] = \
                        self._population[i+1][point1:point2], self._population[i][point1:point2]

    def _mutate_population(self, mutation_scope: list[list] | str, single_mutation: bool, mutation_chance: float) -> None:
        # TODO: make it DRY
        if mutation_chance < 0 or mutation_chance > 1:
            raise BadMutationChance('Mutation chance can not be below 0 or greater than 1.')

        for i in range(len(self._population)):
            if single_mutation:
                if random() <= mutation_chance:
                    mutation_index = choice(range(0, len(self._population[0])))
                    if isinstance(mutation_scope, str):
                        mutation = choice(mutation_scope)
                    else:
                        mutation = choice(mutation_scope[mutation_index])
                    self._population[i][mutation_index] = mutation
            else:
                for j in range(len(self._population[0])):
                    if random() <= mutation_chance:
                        if isinstance(mutation_scope, str):
                            mutation = choice(mutation_scope)
                        else:
                            mutation = choice(mutation_scope[j])
                        self._population[i][j] = mutation

    def fit(self, population: list[list],
            fitness: callable,
            crossover: callable = None,
            generations: int = 20,
            mutator: callable = None,
            single_mutation: bool = True,
            mutation_chance: float = 0.30,
            mutation_scope: list[list] | str = None,
            likelihood_selection: bool = False,
            random_state: int = None):

        if random_state:
            seed(random_state)

        self._population = population.copy()

        for gen in range(generations):
            self._fit_scores = fitness(self._population)
            self._sort_by_fitness()
            self._likelihood = self._get_likelihood()

            # Selection
            if likelihood_selection:
                # TODO: if there is too much saturation; reduce it, maybe try reduced replacement
                # dead_index = choices(range(len(self._fit_scores)), weights=[1-x for x in self._fit_scores], k=1)
                self._population = choices(self._population, weights=self._likelihood, k=len(self._population))
            else:
                # remove the last, make a copy of index 1 on index 2 then switch index 0 and 1
                for i in range(len(self._population)-1, 1, -1):
                    self._population[i] = list(self._population[i-1])
                    self._population
                self._population[0], self._population[1] = self._population[1], self._population[0]

            # Crossover
            if crossover:
                crossover(self._population)
            else:
                self._two_point_crossover()

            # Mutation
            if mutator:
                mutator(self._population)
            else:
                self._mutate_population(mutation_scope, single_mutation, mutation_chance)
