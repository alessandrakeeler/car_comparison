from jobs import q, rd, jdb, update_job_status
import time
import os
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import logging 
import seaborn as sns
logging.basicConfig()

@q.worker
def execute_job(jid):
    logging.critical('Inside worker.')
    update_job_status(jid, 'in progress')
    
    for key in jdb.keys():
        mag = float(jdb.hget(key, 'mag'))

    df = pd.DataFrame(pts('mag',float(mag)))
    df_geo = gpd.GeoDataFrame(df, geometry = gpd.points_from_xy(df.longitude,df.latitude))
    world_data = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    axis = world_data.plot(color = 'sienna', edgecolor = 'black')
    df_geo.plot(ax = axis, color = 'red', markersize=8, alpha=0.5, edgecolor='thistle', linewidth=0.4)

    axis.set_facecolor('powderblue')
    plt.xticks(np.arange(-180, 190, step=10), rotation = 45)
    plt.yticks(np.arange(-90, 100, step=10))
    plt.title(f'Earthquakes With Magnitude >= {mag}')
    plt.savefig(f'EqwksWthMagGrtrThan{mag}.png',dpi=600)
    
    logging.critical(f'EqwksWthMagGrtrThan{mag}.png is saved')
    update_job_status(jid, 'complete')
    
    return 
execute_job()