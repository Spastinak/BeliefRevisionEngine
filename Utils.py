import math
import logging
from operator import neg

from sympy import to_cnf, SympifyError


def removeAll(item, seq):
    """ Return a copy of seq (or string) with all occurrences of item removed.
    """
    if isinstance(seq, str):
        return seq.replace(item, '')
    else:
        return [x for x in seq if x != item]
    
def unique(seq):
    """Remove duplicate elements from seq. Assumes hashable elements."""
    return list(set(seq))

def associate(op, args):
    
    args = dissociate(op, args)
    if len(args) == 0:
        return op.identity
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)
    
    
def conjuncts(args):
    return dissociate("&", [args])

def disjuncts(args):
    return dissociate("|", [args])
    
def dissociate(op, args):
    """given an associative operator and a list of arguments, return a flattened list
    Args:
        op (string): like "&" or "|"
        args (array): [A & B]

    Returns:
        array: [A, B]
    """
    result = []
    
    def collect(subargs):
        for args in subargs:
            if args.op == op:
                collect(args.args)
            else:
                result.append(args) 
    collect(args)    
    return result


