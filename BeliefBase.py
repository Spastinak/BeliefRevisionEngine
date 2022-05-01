import math
from operator import neg
from sortedcontainers import SortedKeyList, SortedList
from sympy import to_cnf, Equivalent

import Utils
from Utils import associate

from entailment import pl_resolution

def checkOrder(order):
    if not(0 <= order <= 1):
        raise ValueError

class BeliefBase:
    def __init__(self):
        self.beliefs = SortedKeyList(key=lambda x: x.order)

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "Belief base is empty"
        return '\n'.join(str(x) for x in self.beliefs)

    def empty(self):
        """ Empty belief base """
        self.beliefs.clear()
        
    def deleteDuplicates(self, newBelief):
        for belief in self.beliefs:
            if belief.formula == newBelief.formula:
                self.beliefs.remove(belief)

    def expand(self, formula, order):
        formula = to_cnf(formula)
        checkOrder(order)
        newBelief = Belief(formula, order)
        self.deleteDuplicates(newBelief)
        
        self.beliefs.add(newBelief)

    def contract(self, formula, order):
        contractionResult = None
        formula = to_cnf(formula)
        # for belief in self.beliefs:
        #     if belief.formula == formula:
        #         self.beliefs.remove(belief)
        entrail = pl_resolution(self, formula)
        for key, value in entrail[1].items():
            keyholder = key
            #for clause in value:
                # if formula == clause:
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
        checkOrder(order)
        entrail = pl_resolution(self, ~formula)
        if entrail[0]:
            if self.contract(~formula, order):
                self.expand(formula, order)
            else:
                raise ValueError
        else:
            self.expand(formula, order)


class Belief:
    def __init__(self, formula, order=None):
        self.formula = formula
        self.order = order



    def __lt__(self, other):
        return self.order < other.order

    def __repr__(self):
        return "Belief: " + str(self.formula) + " with order " + str(self.order)

    def __eq__(self, other):
        if isinstance(other, Belief):
            return self.formula == other.formula and self.order == other.order
        return True


