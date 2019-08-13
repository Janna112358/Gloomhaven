#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 15:25:10 2019

@author: jgoldstein
"""
import numpy as np
import matplotlib.pyplot as plt
from Gloomhaven import max_turns, turns_lost, turns_lost_from_disc

def mask_value(a, val):
    """
    Return masked array version of array a, with all elements equal to val masked.
    
    Parameters
    ----------
    a: numpy array
    val: scalar
    """
    # turn into masked array
    a = np.ma.array(a)
    # mask value
    masked = np.ma.masked_where(a == val, a)
    return masked

def nice_color_plot(array, title=None, cb_label='turns',
                    xlabel='cards in hand', ylabel='cards in discard',
                    save_path='Gloomhaven.png'):
    """
    Make a nice color plot of array.
    
    Parameters
    ----------
    array: numpy array
        can be a masked array
    other: str
        labels and such
    """
    
    fig, ax = plt.subplots(1)
    pcolor = ax.pcolor(array.T)
    cb = fig.colorbar(pcolor)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if title is not None:
        ax.set_title(title)
    cb.set_label(cb_label)
    
    fig.tight_layout()
    fig.savefig(save_path)
    

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
    turns = mask_value(turns, -1)
    
    nice_color_plot(turns, title='Optimizing turns', 
                    cb_label='max turns', save_path='Gloomhaven_turns.png')
    
    
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
    lost = mask_value(lost, -1)
    
    nice_color_plot(lost, title='Preventing damamge', cb_label='turns lost',
                    save_path='Gloomhaven_damage.png')

    
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
    lost2 = mask_value(lost2, -1)
    
    nice_color_plot(lost2, title='Preventing damage from discard', 
                    cb_label='turns lost', save_path='Gloomhaven_damage_from_disc.png')
    
    