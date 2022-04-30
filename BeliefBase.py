import math
from operator import neg
from sortedcontainers import SortedKeyList, SortedList
from sympy import to_cnf, Equivalent
from Utils import associate

from entailment import pl_resolution

class BeliefBase:
    def __init__(self):
        # self.beliefs = []
        self.beliefs = SortedKeyList(key=lambda x: x.order)
        # self.beliefs = SortedList()
        self.tempBeliefs = []
        
    def addTempBeliefs(self, belief, order):
        self.tempBeliefs.append((belief, order))
    
    def reorderBeliefs(self):
        for belief, order in self.tempBeliefs:
            if order > 0:
                belief.order = order
                self.beliefs.add(belief)
        self.tempBeliefs.clear()
        
    
    def add(self, formula, order):
        """
        Add formula to belief base with given order
        """
        formula = to_cnf(formula)
        belief = Belief(formula, order)
        self.beliefs.add(belief)
        

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "Belief base is empty"
        return '\n'.join(str(x) for x in self.beliefs)
            
    def iterateByOrder(self):
        """
        Iterate over the belief base by order
        """
        result = []
        lastOrder = None
        
        for belief in self.beliefs:
            if lastOrder is None:
                result.append(belief)
                lastOrder = belief.order
                continue
            if math.isclose(belief.order, lastOrder):
                result.append(belief)
            else:
                yield lastOrder, result
                result = [belief]
                lastOrder = belief.order
                
        yield lastOrder, result
        
        
        
        

       
    def degree(self, formula):
        if pl_resolution([], formula):
            return 1
        base = []
        for order, row in self.iterateByOrder():
            base += [x.formula for x in row]
            if pl_resolution(base, formula):
                return order
        return 0
        
        
        
        
    
    def empty(self):
        """ Empty belief base """
        self.beliefs.clear()
        
        
    def expand(self, formula, order):
        newFormula = to_cnf(formula)
        if not pl_resolution([], ~newFormula):
            if pl_resolution([], newFormula):
                order = 1
            else: 
                for belief in self.beliefs:
                    oldFormula = belief.formula
                    if belief.order > order:
                        continue
                    
                    degree = self.degree(oldFormula >> newFormula)
                    if (pl_resolution([], Equivalent(newFormula, oldFormula)) or belief.order <= order < degree):
                        self.addTempBeliefs(belief, order) 
                    else: 
                        self.addTempBeliefs(belief, degree)
                self.reorderBeliefs()
        
        
        
        
    def contract(self, formula, order):
        newFormula = to_cnf(formula)
        
        for belief in self.beliefs:
            oldFormula = belief.formula
            if belief.order > order:
                degreeNew = self.degree(newFormula)
                newOrOld = associate("|", [oldFormula, newFormula])
                degreeNewOrOld = self.degree(newOrOld)
                if degreeNew == degreeNewOrOld:
                    self.addTempBeliefs(belief, order)
        self.reorderBeliefs()
        
        
        
    def revise(self, formula, order):
        formula = to_cnf(formula)
        degree = self.degree(formula)
        
        if not pl_resolution([], ~formula):
            if pl_resolution([], formula):
                order = 1
            elif order <= degree:
                self.contract(formula, order)
            else:
                self.contract(~formula, 0)
                self.expand(formula, order)
    
    

class Belief:
    def __init__(self, formula, order):
        self.formula = formula
        self.order = order
        ## self.order = order
        
    # def __hash__(self):
    #     return hash(self.formula)
    def __lt__(self, other):
        return self.order < other.order
    def __repr__(self):
        return "Belief: " + str(self.formula) + " with order " + str(self.order)
    def __eq__(self, other):
        return self.formula == other.formula and self.order == other.order
    
# def isclose(a, b):
#     return math.isclose(a, b, rel_tol=1e-09)