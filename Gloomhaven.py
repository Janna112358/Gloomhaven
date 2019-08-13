#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 13:40:41 2019

@author: jgoldstein
"""
import numpy as np
import matplotlib.pyplot as plt

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
    if n == 2:
        return 1
    else:
        return n//2 + max_turns_recursive(n-1)


def max_turns(n, m):
    """
    Parameters
    ----------
    n: int
        cards in hand
    m: int
        cards in discard (not lost)
    """
    return (n//2) + max_turns_initial(n+m-1)

def turns_lost(n, m):
    """
    Number of turns lost by preventing damage. Assumes you always lose one card 
    from hand if possible, otherwise 2 cards from discard
    """
    if n == 0:
        return max_turns(n, m) - max_turns(n, m-2)
    else:
        return max_turns(n, m) - max_turns(n-1, m)

def turns_lost_from_disc(n, m):
    """
    Number of turns lost by preventing damage, but always choosing to lose two
    cards from discard rather than one from hand.
    """
    return max_turns(n, m) - max_turns(n, m-2)

if __name__ == '__main__':
    
    max_cards = 12
    all_hand = np.arange(0, max_cards+1, dtype=int)
    all_disc = np.arange(0, max_cards+1, dtype=int)
    
    # compute max turns for all combinations of hand and discard
    turns = np.zeros((len(all_hand), len(all_disc)))
    for i, j in np.ndindex(turns.shape):
        hand = all_hand[i]
        disc = all_disc[j]
        
        # mask (with -1) if hand+disc > max cards
        if hand + disc > max_cards:
            turns[i, j] = -1
            
        else:
            turns[i, j] = max_turns(hand, disc)
            
    # mask properly
    turns = np.ma.array(turns)
    turns = np.ma.masked_where(turns == -1, turns)
    
    # plot
    fig, ax = plt.subplots(1)
    pcolor = ax.pcolor(turns.T)
    cb = fig.colorbar(pcolor)
    
    ax.set_xlabel('cards in hand')
    ax.set_ylabel('cards in discard')
    cb.set_label('max turns')
    
    fig.tight_layout()
    fig.savefig('Gloomhaven_turns.png')
    
    
    # compute turns lost for all (reasonable) combinations of hand and discard
    lost = np.zeros_like(turns)
    for i, j in np.ndindex(lost.shape):
        hand = all_hand[i]
        disc = all_disc[j]
        
        # mask (with -1) if hand+disc > max cards
        if hand + disc > max_cards:
            lost[i, j] = -1
        # also mask if not enough cards to prevent damage
        elif hand == 0 and disc < 2:
            lost[i, j] = -1
        
        else:
            lost[i, j] = turns_lost(hand, disc)
            
    
    # mask properly
    lost = np.ma.array(lost)
    lost = np.ma.masked_where(lost == -1, lost)
    
    # plot
    fig2, ax2 = plt.subplots(1)
    pcolor2 = ax2.pcolor(lost.T)
    cb2 = fig2.colorbar(pcolor2)
    
    ax2.set_xlabel('cards in hand')
    ax2.set_ylabel('cards in discard')
    cb2.set_label('turns lost')
    ax2.set_title('preventing damage')
    
    fig2.tight_layout()
    fig2.savefig('Gloomhaven_damage.png')
    
    # compute turns lost for all combination of hand and discard, if always 
    # losing cards from disc instead of hand
    
    lost2 = np.zeros_like(turns)
    for i, j in np.ndindex(lost2.shape):
        hand = all_hand[i]
        disc = all_disc[j]
        
        # mask (with -1) if hand+disc > max cards
        if hand + disc > max_cards:
            lost2[i, j] = -1
        # also mask if not enough cards to prevent damage
        elif hand == 0 and disc < 2:
            lost2[i, j] = -1
        
        else:
            lost2[i, j] = turns_lost_from_disc(hand, disc)
            
    
    # mask properly
    lost2 = np.ma.array(lost2)
    lost2 = np.ma.masked_where(lost2 == -1, lost2)
    
    # plot
    fig3, ax3 = plt.subplots(1)
    pcolor3 = ax3.pcolor(lost2.T)
    cb3 = fig3.colorbar(pcolor3)
    
    ax3.set_xlabel('cards in hand')
    ax3.set_ylabel('cards in discard')
    cb3.set_label('turns lost')
    ax3.set_title('preventing damage from disc')
    
    fig3.tight_layout()
    fig3.savefig('Gloomhaven_damage_from_disc.png')
    
    
    