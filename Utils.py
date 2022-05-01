
from sympy.logic.boolalg import Or, And


# def removeItem(item, seq):
#     """ Return a copy of seq (or string) with all occurrences of item removed.
#     """
#     return [x for x in seq if x != item]
def removeDuplicates(item,seq):
    return [x for x in seq if x.formula != item.formula]

# def removeAll(item, seq):
#     """ Return a copy of seq (or string) with all occurrences of item removed.
#     """
#     if isinstance(seq, str):
#         return seq.replace(item, '')
#     else:
#         return [x for x in seq if x != item]
def removeall(item, seq):
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
    return dissociate(And, [args])

def disjuncts(args):
    return dissociate(Or, [args])
    
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
        for arg in subargs:
            if isinstance(arg, op):
                collect(arg.args)
            else:
                result.append(arg) 
    collect(args)    
    return result