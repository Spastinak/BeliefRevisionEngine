import math

class BeliefBase:
    def __init__(self) -> None:
        pass
    
    def add(self, formula, order):
        pass
    def degree(self, formula):
        pass
    def clear(self):
        pass
    def expand(self, formula):
        pass
    def contract(self, formula):
        pass
    def revise(self, formula, order):
        pass
    
    

class Belief:
    def __init__(self, formula, order=None):
        self.formula = formula
        self.order = order
        
    def __hash__(self):
        return hash(self.formula)
    def __repr__(self):
        return "Belief: " + str(self.formula) + " with order " + str(self.order)
    def __eq__(self, other):
        return self.formula == other.formula and self.order == other.order
    
def isclose(a, b):
    return math.isclose(a, b, rel_tol=1e-09)