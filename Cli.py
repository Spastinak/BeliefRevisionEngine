import argparse
import logging

from sympy import to_cnf, SympifyError

from BeliefBase import BeliefBase


## from belief_base import BeliefBase


def printHelp():
    print(
        """
    ####################################
      Belief Revision Agent - Group 45 
    ####################################
    
    available commands:
    r: Belief revison
    e: Empty belief base
    p: Print belief base
    h: Print help dialog
    q: Quit    
    """)


def clearConsole():
    print('\n' * 150)





def handleInput(beliefBase):
    command = input("Select command: ")
    command = command.lower()
    if command == "r":
        print("Revision")
        formula = input("Please enter formula: ")
        try:
            formula = to_cnf(formula)
            print(formula)
            order = input("Please enter order (real number from 0 to 1): ")
            beliefBase.revise(formula, float(order))
            clearConsole()
            printHelp()
        except SympifyError:
            print("Formula is not valid")
        except ValueError:
            print("Order is not valid")


    elif command == "e":
        print("Empty belief base")
        beliefBase.empty()
        clearConsole()
        printHelp()

    elif command == "p":
        clearConsole()
        print("belief base:")
        print(beliefBase)
        print("\n")


    elif command == "h":
        clearConsole()
        printHelp()

    elif command == "q":
        print("Quitting")
        exit()

    else:
        clearConsole()
        print("Unknown command. Type 'h' for help")

    handleInput(beliefBase)


if __name__ == "__main__":
    beliefBase = BeliefBase()
    printHelp()
    handleInput(beliefBase)
