# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 11:20:51 2020

@author: guillaume
"""

import numpy as np
import xarray as xr
import bottleneck
from scipy import stats

def covariance_gufunc(x, y):
    return ((x - x.mean(axis=-1, keepdims=True))
            * (y - y.mean(axis=-1, keepdims=True))).mean(axis=-1)

def pearson_correlation_gufunc(x, y):
    return covariance_gufunc(x, y) / (x.std(axis=-1) * y.std(axis=-1))

def spearman_correlation_gufunc(x, y):
    x_ranks = bottleneck.rankdata(x, axis=-1)
    y_ranks = bottleneck.rankdata(y, axis=-1)
    return pearson_correlation_gufunc(x_ranks, y_ranks)

def spearman_correlation(x, y, dim):
    return xr.apply_ufunc(
        spearman_correlation_gufunc, x, y,
        input_core_dims=[[dim], [dim]],
        dask='parallelized',
        output_dtypes=[float])
    
    
rs = np.random.RandomState(0)
array1 = xr.DataArray(rs.randn(1000, 100000), dims=['place', 'time'])  # 800MB
array2 = array1 + 0.5 * rs.randn(1000, 100000)

r1 = spearman_correlation(array1, array2, 'time')

chunked1 = array1.chunk({'place': 10})
chunked2 = array2.chunk({'place': 10})
r2 = spearman_correlation(chunked1, chunked2, 'time').compute()
#%time_ = r1.compute()
#_ = r2.compute()

r3, p3 = stats.spearmanr(array1,array2) 
test= array1.values