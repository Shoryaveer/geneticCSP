from CSP2gen import Cgen
import pprint


def fitness(population):
    satisfy = 0
    retList = []
    for pop in population:
        satisfy = 0
        A, B, C, D, E, F, G, H = pop

        if A > G:
            satisfy += 1
        if A <= H:
            satisfy += 1
        if abs(F - B) == 1:
            satisfy += 1
        if G < H:
            satisfy += 1
        if abs(G - C) == 1:
            satisfy += 1
        if abs(H - C) % 2 == 0:
            satisfy += 1
        if H != D:
            satisfy += 1
        if D >= G:
            satisfy += 1
        if D != C:
            satisfy += 1
        if E != C:
            satisfy += 1
        if E < D - 1:
            satisfy += 1
        if E != H - 2:
            satisfy += 1
        if G != F:
            satisfy += 1
        if H != F:
            satisfy += 1
        if C != F:
            satisfy += 1
        if D != F - 1:
            satisfy += 1
        if abs(E - F) % 2 == 1:
            satisfy += 1
        retList.append(satisfy)

    return retList


sample_population = [
    [1, 1, 1, 1, 1, 1, 1, 1],
    [2, 2, 2, 2, 2, 2, 2, 2],
    [3, 3, 3, 3, 3, 3, 3, 3],
    [4, 4, 4, 4, 4, 4, 4, 4],
    [1, 2, 3, 4, 1, 2, 3, 4],
    [4, 3, 2, 1, 4, 3, 2, 1],
    [1, 2, 1, 2, 1, 2, 1, 2],
    [3, 4, 3, 4, 3, 4, 3, 4]
]

cgen = Cgen()

cgen.fit(sample_population,
         fitness=fitness,
         generations=20,
         mutation_chance=.7,
         single_mutation=False,
         likelihood_selection=False,
         mutation_scope='1234',
         random_state=999)

pprint.pprint(cgen._population)
pprint.pprint(cgen._likelihood)
pprint.pprint(cgen._fit_scores)
