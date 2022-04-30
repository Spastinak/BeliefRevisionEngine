from sympy import to_cnf

from Utils import conjuncts, associate, disjuncts, removeAll, removeDuplicates, removeItem, unique


# def entailment(kb, formula):
#     """
#     Check entailment of a formula in a knowledge base.
#     """
#     formula = to_cnf(formula)
#     clauses = []
#     for i in kb:
#         clauses += conjuncts(i)
    
#     pl_resolution(clauses, formula)
    
         
    
    
    
def pl_resolution(kb, alpha):
    """[figure 7.12] from the book.
    Propositional-logic resolution: say if a KB entails a given alpha. [Figure 7.12]

    Args:
        kb (knowlageBase): horn clause knowledge base
        alpha: clause
    """
    clauses = []
    new = set()
    alpha = to_cnf(alpha)
    for i in kb:
        clauses += conjuncts(i)
    
    clauses += conjuncts(to_cnf(~alpha))
    
    
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j])
                 for i in range(n) for j in range(i+1, n)]
        for ci, cj in pairs:
            resolvents = pl_resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))
        if new.issubset(set(clauses)):
            return False
        for i in new:
            if i not in clauses:
                clauses.append(i)
            

# def pl_resolve(ci, cj):
#     """returns the set of all possible clauses obtained by resolving its two inputs."""
#     clauses = []
#     resoulved = False 
#     for di in disjuncts(ci):
#         for dj in disjuncts(cj):
#             if di == ~dj or ~di == dj:
#                 clauses.append(associate('|', unique(removeAll(di, disjuncts(ci)) + removeAll(dj, disjuncts(cj)))))
#                 resoulved = True
#     if not resoulved:
#         clauses.append(associate('|', unique(disjuncts(ci) + disjuncts(cj))))
        
#     return clauses
def pl_resolve(ci, cj):
    clauses = []
    dci = disjuncts(ci)
    dcj = disjuncts(cj)
    
    for di in dci:
        for dj in dcj:
            if di == ~dj or dj == ~di:
                reso = removeItem(di, dci) + removeItem(dj, dcj)
                reso = removeDuplicates(reso)
                newClause = associate('|', reso)
                clauses.append(newClause)
    return clauses