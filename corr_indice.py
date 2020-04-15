# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 16:18:52 2019

@author: guillaume
"""
from scipy import stats
import matplotlib.pylab as plt

def corr_pearson(x, y, **kws):
    r, p = stats.pearsonr(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
   # r, _ = stats.spearmanr(x, y)
    ax = plt.gca()   
    pos = (.5, .9) if kws['label'] == 'RCMS_Histo' else (.5, .8) if kws['label'] == 'RCMS_rcp45' else (.5, .7) 
    color2='green' if kws['label'] == 'RCMS_Histo' else 'blue' if kws['label'] == 'RCMS_rcp45'  else  'red'  
    
    ax.annotate("Pearson:",xy=(0, .9), xycoords=ax.transAxes, fontweight='bold')                                                          
    ax.annotate("r_p = {:.2f}".format(r) + p_stars,
                xy=pos, xycoords=ax.transAxes, color=color2, fontweight='bold')
    
    
def corr_spearman(x, y, **kws):
    r, p = stats.spearmanr(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
   # r, _ = stats.spearmanr(x, y)
    ax = plt.gca()  
    pos = (.5, .55) if kws['label'] == 'RCMS_Histo' else (.5, .45) if kws['label'] == 'RCMS_rcp45'  else (.5, .35)
    color2='green' if kws['label'] == 'RCMS_Histo' else 'blue' if kws['label'] == 'RCMS_rcp45'  else  'red' 
    ax.annotate("Spearman:",xy=(0, .55), xycoords=ax.transAxes, fontweight='bold') 
    ax.annotate("r_s = {:.2f}".format(r) + p_stars,
                xy=pos, xycoords=ax.transAxes, color=color2, fontweight='bold')


def corr_kendall(x, y, **kws):
    r, p = stats.kendalltau(x, y)
    p_stars = ''
    if p <= 0.05:
        p_stars = '*'
    if p <= 0.01:
        p_stars = '**'
    if p <= 0.001:
        p_stars = '***'
   # r, _ = stats.spearmanr(x, y)
    ax = plt.gca()   
    pos = (.5, .2) if kws['label'] == 'RCMS_Histo' else (.5, .1) if kws['label'] == 'RCMS_rcp45'  else (.5, .0)
    color2='green' if kws['label'] == 'RCMS_Histo' else 'blue' if kws['label'] == 'RCMS_rcp45'  else  'red'                                                                 
    ax.annotate("Kendall:",xy=(0, .2), xycoords=ax.transAxes, fontweight='bold')
    ax.annotate("r_k = {:.2f}".format(r) + p_stars,
                xy=pos, xycoords=ax.transAxes, color=color2, fontweight='bold')