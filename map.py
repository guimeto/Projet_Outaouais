# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 09:34:22 2019

@author: guillaume
"""


# Get the metadata for the most recent NEXRAD image from JSON file.
# https://github.com/blaylockbk/pyBKB_v3/blob/master/BB_maps/cartopy_NEXRAD-mosaic-from-Iowa.ipynb

from datetime import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import requests

def get_timestamp():
    f = requests.get('https://mesonet.agron.iastate.edu/data/gis/images/4326/USCOMP/n0q_0.json').json()
    validDATE = datetime.strptime(f['meta']['valid'], '%Y-%m-%dT%H:%M:%SZ')
    return validDATE

print('Latest Image:', get_timestamp())
print('Current Time:', datetime.utcnow())

diff = (datetime.utcnow()-get_timestamp())
print('Difference (minutes):', diff.seconds/60)

fig = plt.figure(figsize=(15, 5))

ax = fig.add_subplot(1, 1, 1,
                     projection=ccrs.LambertConformal(central_longitude=-100))
ax.add_feature(cfeature.COASTLINE.with_scale('50m'))
ax.add_feature(cfeature.BORDERS.with_scale('50m'))
ax.add_feature(cfeature.STATES.with_scale('50m'))

# Date string format for data reques

ax.set_title('Most Recent Time', fontweight='bold', loc='left')
ax.set_title('%s' % get_timestamp().strftime('%H:%M UTC %d %b %Y'), loc='right')
ax.add_wms(wms='https://mesonet.agron.iastate.edu/cgi-bin/wms/nexrad/n0q-t.cgi?',
           layers='nexrad-n0q-wmst',
           wms_kwargs={'transparent':True}, zorder=10)
# ^ For current time (most recent time in last 5 minutes), leave the 'time' 
#   wms_kwargs unassigned. Transparetn should be True by default, but it
#   doesn't hurt to be explicit.

ax.set_extent([-120, -75, 23, 50])

fig.subplots_adjust(wspace=0.02)
