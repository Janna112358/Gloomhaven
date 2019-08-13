#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:40:41 2019

@author: jgoldstein
"""
### docstring convenience stuff ###

# so we don't repeat bits of docstring many times, use this decorator
# to add standard bits of docstring for parameters and return values
def add_doc(doc):
    def decorator(func):
        func.__doc__ += doc
        return func
    return decorator


std_params_doc = """

    Parameters
    ----------
    n: int
        cards in hand
    m: int
        cards in discard (not lost)
"""

turns_returns_doc = """
    Returns
    -------
    int: max number of turns (not counting long rests)
"""

lost_returns_doc = """
    Returns
    -------
    int: number of turns lost
"""

### Gloomhaven functions ###

@add_doc(turns_returns_doc)
def max_turns_initial(n):
    """
    Maximum number of turns you can play, assuming no shenanigans, if you start
    with n cards in hand, no cards in discard. This also assumes you don't 
    loose cards through card abilities, damage prevention, and that you only 
    rest when necessary (i.e. once you've played your hand).
    
    Parameters
    ----------
    n: int
    """
    # n even
    if (n%2 == 0):
        return (n//2)**2
    # n odd
    else:
        return (n-1)//2 * (n+1)//2
    
    
@add_doc(turns_returns_doc)
def max_turns_recursive(n):
    """
    Same as max_turns_initial, but use a recursive implementation.
    
    Parameters
    ----------
    n: int
    """
    if n == 2:
        return 1
    else:
        return n//2 + max_turns_recursive(n-1)


@add_doc(std_params_doc + turns_returns_doc)
def max_turns(n, m):
    """
    Maximum number of turns you can play (same assumptions as max_turns_initially),
    for cards in hand and discard.
    """
    return (n//2) + max_turns_initial(n+m-1)


@add_doc(std_params_doc + lost_returns_doc)
def turns_lost(n, m):
    """
    Number of turns lost by preventing damage. Assumes you always lose one card 
    from hand if possible, otherwise 2 cards from discard
    """
    if n == 0:
        return max_turns(n, m) - max_turns(n, m-2)
    else:
        return max_turns(n, m) - max_turns(n-1, m)
    

@add_doc(std_params_doc + lost_returns_doc)
def turns_lost_from_disc(n, m):
    """
    Same as turns_lost, except assumes you always choose to lose 2 cards from
    discard, instead of from hand where possible.
    """
    return max_turns(n, m) - max_turns(n, m-2)


@add_doc(std_params_doc + lost_returns_doc)
def turns_lost_early_rest(n, m):
    """
    Compute number of turns lost by resting right now. Compare to max turns 
    where we rest only once we have to.
    """
    
    max_num_turns = max_turns(n, m)
    rest_num_turns = max_turns(n+m-1, 0)
    
    return max_num_turns - rest_num_turns
    
    

