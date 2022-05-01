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
        
    
    # def add(self, formula, order):
    #     """
    #     Add formula to belief base with given order
    #     """
    #     formula = to_cnf(formula)
    #     belief = Belief(formula, order)
    #     self.beliefs.add(belief)
        

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
        
        
        
        

       
    def degree(self, query):

        if pl_resolution([], query):  # is query a tautology
            return 1

        base = []
        for order, row in self.sort_beliefs():  # does anything in our belief base entail our query
            base += [b.query for b in row]
            if pl_resolution(base, query):
                return order
        return 0  # returns 0 if none of the above is true
        
        
        
        
    
    def empty(self):
        """ Empty belief base """
        self.beliefs.clear()
        
        
    def expand(self, formula, order):
            formula = to_cnf(formula)
            newBelief = Belief(formula, order)
            for belief in self.beliefs:
                belief.order += 1
            # self.beliefs.append(newBelief)
            self.beliefs.add(newBelief) 

            
        
        
        
        
    def contract(self, formula, order):
        contractionResult = None
        formula = to_cnf(formula)
        for belief in self.beliefs:
            if belief.formula == formula:
                self.beliefs.remove(belief)
        entrail = pl_resolution(self,formula)
        for key, value in entrail[1].items():
            keyholder = key
            for clause in value:
                if formula == clause:
                    for belief in self.beliefs:
                        if belief.formula == keyholder:
                            if belief in self.beliefs and belief.order < order:
                                self.beliefs.remove(belief)
                                contractionResult = True
                            elif belief in self.beliefs and belief.order >= order:
                                # TODO ValueError
                                contractionResult = False
                            else:
                                # TODO SympifyError
                                contractionResult = False
        return contractionResult
                                
                            
        
        
        
        
    def revise(self, formula, order):
        formula = to_cnf(formula)
        
        entrail = pl_resolution(self, ~formula)
        if entrail[0]:
            if self.contract(~formula, order):
                self.expand(formula, order)
            else:
                # TODO ValueError
                pass
        else:
            self.expand(formula, order)
            
    
    

class Belief:
    def __init__(self, formula, order=None):
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
        return self.order == other.order and self.formula == other.formula
    
    
    
# def isclose(a, b):
#     return math.isclose(a, b, rel_tol=1e-09)