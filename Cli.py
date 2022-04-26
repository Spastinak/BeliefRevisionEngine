import argparse
import logging

from sympy import to_cnf, SympifyError

## from belief_base import BeliefBase



def printHelp():
    print(
    """
    available commands:
    r: Belief revison
    d: Calculate degree of belief
    e: Empty belief base
    p: Print belief base
    h: Print help dialog
    q: Quit    
    """)

def handleInput(beliefBase):
    command = input("Select command: ")
    command = command.lower()
    if command == "r":
        print("Revision")
        formula = input("Please enter formula: ")
        try:
            formula = to_cnf(formula)
            print (formula)
            ##order = input("Please enter order (real number from 0 to 1): ")
            ##beliefBase.revise(formula, float(order))
        except SympifyError:
            print("Formula is not valid")
        except ValueError:
            print("Order is not valid")
          
    elif command == "d":
        print("Degree of belief")
        formula = input("Please enter formula: ")
        
        formula = to_cnf(formula)
        ## TODO make belief base class and method
        ##print(beliefBase.degree(formula))
        
    elif command == "e":
        print("Empty belief base")
        beliefBase.empty()
        
    elif command == "p":
        print("Print belief base")
        print(beliefBase)
        
    elif command == "h":
        printHelp()
        
    elif command == "q":
        print("Quitting")
        exit()
        
    else:
        print("Unknown command. Type 'h' for help")
    
    handleInput(beliefBase)

printHelp()
handleInput(beliefBase=None)
