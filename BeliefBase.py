import math
from sortedcontainers import SortedKeyList, SortedList
from sympy import to_cnf

import Utils
import entailment


class BeliefBase:
    def __init__(self):
        # self.beliefs = []
        # self.beliefs = SortedList(key=lambda x: x.order)
        self.beliefs = []
        self.order = {}

    def add(self, formula, order):
        """
        Add formula to belief base with given order
        """
        formula = to_cnf(formula)
        belief = Belief(formula, order)
        self.beliefs.append(belief)

    def __repr__(self):
        if len(self.beliefs) == 0:
            return "Belief base is empty"
        return '\n'.join(str(x) for x in self.beliefs)

    def degree(self, formula):
        pass

    def clear(self):
        pass

    """
    Expanding a belief set without making any revision. Simply adding new beliefs.
    If belief set is: A, B --> C
    And we expand with: D
    New belief set is: A, B --> C, D
    """

    def empty(self):
        """ Empty belief base """
        self.beliefs.clear()

    def expand(self, formula, order):
        formula = to_cnf(formula)
        belief = Belief(formula, order)
        self.beliefs.append(belief)

    """
    Contract is removing a belief. The belief can be rooted in many other beliefs.
    If belief set is: A, B --> C
    We contract with: C
    New belief set is: A, !B
    """

    def contract(self, formula):
        formula = to_cnf(formula)

        for i in self.beliefs:
            if formula == i.formula:
                self.beliefs.pop(formula)

    def revise(self, formula, order):
        formula = to_cnf(formula)
        notFormula = to_cnf(~formula)
        flag = True

        self.beliefs = Utils.removeAllDuplicates(Belief(formula,order), self.beliefs)


        newBeliefBase = []
        beliefOrder = []
        for i in self.beliefs:
            if notFormula != i.formula:
                newBeliefBase.append(i)
            else:
                beliefOrder.append(i)

        for i in beliefOrder:
            if i.order > order:
                flag = False
                newBeliefBase.extend(beliefOrder)

        self.beliefs = newBeliefBase
        if flag:
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
