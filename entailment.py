from sympy import to_cnf
from sympy.logic.boolalg import Or, And

from Utils import conjuncts, associate, disjuncts, removeall, unique


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
    alpha = to_cnf(alpha)
    clauses = []
    beliefDict = {}

    for belief in kb.beliefs:
        beliefDict[to_cnf(belief.formula)] = to_cnf(conjuncts(belief.formula))
        clauses += conjuncts(belief.formula)
    
    clauses += conjuncts(to_cnf(~alpha))
    
    new = set()
    
    while True:
        n = len(clauses)
        pairs = [(clauses[i], clauses[j]) for i in range(n) for j in range(i+1, n)]
        
        for ci, cj in pairs:
            resolvents = pl_resolve(ci, cj)
            new = new.union(set(resolvents))
            if False in resolvents:
                return True, beliefDict
            
        if new.issubset(set(clauses)):
            return False, beliefDict
        for c in new:
            if c not in clauses:
                clauses.append(c)
            

def pl_resolve(ci, cj):
    clauses = []
    disjunction_ci = disjuncts(ci)
    disjunction_cj = disjuncts(cj)
    
    for literal_i  in disjunction_ci:
        for literal_j  in disjunction_cj:
            if literal_i == ~literal_j or ~literal_i == literal_j:
                remaining = removeall(literal_i, disjunction_ci) + removeall(literal_j, disjunction_cj)
                remaining = unique(remaining)
                new_clause = associate(Or, remaining)
                clauses.append(new_clause)
    return clauses

