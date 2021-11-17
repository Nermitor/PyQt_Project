def prod(g):
    return iter(sorted([(el1, el) for el1 in g for el in g if el1 != el], key=lambda x: x[0]))
