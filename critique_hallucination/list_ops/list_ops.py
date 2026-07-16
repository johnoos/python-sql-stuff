"""Implements common list behaviour without using built-in methods.
New concepts: 
1) variable number of arguments, and 
2) recursive functions"""

def append(list1, list2):
    """Concatenates two lists"""
    mylist = list1 + []
    for item in list2:
        mylist = mylist + [item]
    return mylist

def concat(lists):
    result = []
    for sublist in lists:
        result = append(result, sublist)  # Reuses your own custom append function
    return result

def filter(predicate, in_list):
    """a predicate is a function that takes one argument and 
    returns either True or False"""
    out_list = []
    for item in in_list:
        if predicate(item):
            out_list = out_list + [item]
    return out_list

def length(alist):
    """returns the length of a list"""
    counter = 0
    for _, _ in enumerate(alist):
        counter += 1
    return counter

def map(afunc, inlist):
    """ apply provided function to each list item """
    outlist = []
    for item in inlist:
        outlist = outlist + [afunc(item)]
    return outlist

def foldl(afunc, alist, initval):
    """ fold into accumulated value from the left """
    cumval = initval
    if alist == []:
        return initval
    for item in alist:
        cumval = afunc(cumval, item)
    return cumval
    
def foldr(afunc, alist, initval):
    """ fold into accumulated value from the right """
    
    if alist == []:
        return initval
    
    cumval = initval
    for item in range(len(alist)-1, -1, -1):
        cumval = afunc(cumval, alist[item])
        print(f"DEBUG foldr()-n: cumval: {cumval}")
    return cumval

def reverse(alist):
    """ reverse list """        
    outlist = []
    if alist == []:
        return []
    for idx in range(len(alist)-1, -1, -1):
        outlist = outlist + [alist[idx]]
    return outlist    