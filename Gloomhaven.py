#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:40:41 2019

@author: jgoldstein
"""
def max_turns_initial(n):
    """
    Maximum number of turns you can play, assuming no shenanigans, if you start
    with n cards in hand, no cards in discard. This also assumes you don't 
    loose cards through card abilities, damage prevention, and that you only 
    rest when necessary (i.e. once you've played your hand).
    
    Parameters
    ----------
    n: int
    
    Returns
    -------
    int: max number of turns (not counting long rests)
    """
    # n even
    if (n%2 == 0):
        return (n//2)**2
    # n odd
    else:
        return (n-1)//2 * (n+1)//2
    
    
def max_turns_recursive(n):
    """
    Same as max_turns_initial, but use a recursive implementation.
    
    Parameters
    ----------
    n: int
    
    Returns
    -------
    int: max number of turns (not counting long rests)
    """
    if n == 2:
        return 1
    else:
        return n//2 + max_turns_recursive(n-1)


def max_turns(n, m):
    """
    Maximum number of turns you can play (same assumptions as max_turns_initially),
    for cards in hand and discard.
    
    Parameters
    ----------
    n: int
        cards in hand
    m: int
        cards in discard (not lost)
        
    Returns
    -------
    int: max number of turns (not counting long rests)
    """
    return (n//2) + max_turns_initial(n+m-1)


def turns_lost(n, m):
    """
    Number of turns lost by preventing damage. Assumes you always lose one card 
    from hand if possible, otherwise 2 cards from discard
    
    Parameters
    ----------
    n: int
        cards in hand
    m: int
        cards in discard (not lost)
        
    Returns
    -------
    int: number of turns lost
    """
    if n == 0:
        return max_turns(n, m) - max_turns(n, m-2)
    else:
        return max_turns(n, m) - max_turns(n-1, m)
    

def turns_lost_from_disc(n, m):
    """
    Same as turns_lost, except assumes you always choose to lose 2 cards from
    discard, instead of from hand where possible.
    
    Parameters
    ----------
    n: int
        cards in hand
    m: int
        cards in discard (not lost)
        
    Returns
    -------
    int: number of turns lost
    """
    return max_turns(n, m) - max_turns(n, m-2)

