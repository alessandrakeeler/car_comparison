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
    """
    Worker to execute the graphing job 
    Args:
        jid(string): describes the job id of the job to be executed by the worker 
    Returns:
        None
    """
    logging.critical('Inside worker.')
    update_job_status(jid, 'in progress')

    data = jdb.hgetall(f'job.{jid}')
    
    feature1 = data['feature1']
    feature2 = data['feature2']
    comparison_factor = data['comparison_factor']

    features = [
        "make",
        "model",
        "vehicle_class",
        "engine_size(l)",
        "cylinders",
        "transmission",
        "fuel_type",
        "fuel_consumption_(city_(l/100_km)",
        "fuel_consumption(hwy_(l/100_km))",
        "fuel_consumption(comb_(l/100_km))",
        "fuel_consumption(comb_(mpg))",
        "co2_emissions(g/km)",
        "co2_rating",
        "smog_rating",
    ]

    df = pd.DataFrame(columns=features)
    for key in rd.keys():
        make_dict = json.loads(rd.get(key))
        for model in make_dict:
            list_items = list((make_dict[model]).items())
            data_list = [item[1] for item in list_items]
            df = df.append(pd.Series(data_list, index=df.columns), ignore_index=True)

    if comparison_factor == 'make':
        sns.set(rc={"figure.figsize": (11.7, 8.27)})
        scatter = sns.scatterplot(data=df, x=feature1, y=feature2, hue=comparison_factor)
        fig = scatter.get_figure()
        plt.legend(fontsize="small", loc=2, bbox_to_anchor=(1, 1.16))

    else: 
        sns.set(rc={"figure.figsize": (11.7, 8.27)})
        scatter = sns.scatterplot(data=df, x=feature1, y=feature2, hue=comparison_factor)
        fig = scatter.get_figure()
        plt.legend(fontsize="small", loc=2)

    img_path = f"/{feature1}_vs_{feature2}_compared_on_{comparison_factor}.png"
    fig.savefig(image_path)
    
    with open(image_path, 'rb') as f:
        img = f.read()

    img_db.hset(f'job.{jid}', 'image', img) 
    jdb.hset(f'job.{jid}', 'status', 'finished')
    update_job_status(jid, 'complete')
    
    return 
execute_job()