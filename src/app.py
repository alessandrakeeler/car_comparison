from flask import Flask, jsonify, request
import logging
import xmltodict
import pandas as pd
import json
import statistics as s
import os
import redis
import seaborn as sns
import matplotlib.pyplot as plt
from helper_functions import make_exists, model_exists
from jobs import *

""" redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception() """

rd = redis.StrictRedis(host="127.0.0.1", port=6413, db=13)


app = Flask(__name__)


@app.route("/data", methods=["POST", "GET"])
def load_data():
    """
    POST : Loads fuel consumption data into Redis
    GET : Returns fuel consumption data as a dictionary 

    """
    logging.info("Reading in fuel consumption data.")


    if request.method == "POST":
        rd.flushdb()

        data = {}
        df = pd.read_csv("fuel_ratings.csv")
        df = df.applymap(lambda s: s.replace(" ", "_") if type(s) == str else s)
        df = df.applymap(lambda s: s.lower() if type(s) == str else s)

        columns = [c.replace(" ", "_").lower() for c in list(df.columns)]
        col = [columns[i] for i in range(1, len(columns))]
        df.columns = columns

        for make in df["make"].unique():
            out = {
                make: df.loc[df["make"] == make]
                .groupby("model")[col]
                .last()
                .to_dict(orient="index")
            }
            if make == "acura":
                data = {"make": out}
            else:
                data["make"][make] = out[make]
        final_data = data["make"]

        for make in final_data:
            rd.set(make, json.dumps(final_data[make]))

        return "Data loaded into redis \n"

    elif request.method == "GET":
        makes = []
        for item in rd.keys():
            makes.append({item.decode("utf-8"): json.loads(rd.get(item))})
        return json.dumps(makes, indent=4)

    else:
        return "Method only supports POST and GET \n"


@app.route("/makes", methods=["GET"])
def get_makes():
    """
    Outputs all makes in dataset.
    """
    make_list = []
    for key in rd.keys():
        make_list.append(key.decode("utf-8"))
    return jsonify(make_list)


@app.route("/<make>/<model>/features", methods=["GET"])
def get_arguments(make, model):
    """
    Ouputs all possible features for each make and model
    """

    make_dict = json.loads(rd.get(make))
    return jsonify(list(make_dict[model].keys()))


@app.route("/<make>/models", methods=["GET"])
def models_for_make(make: str):
    """
    Outputs all models under a specified make.

    """

    make_dict = json.loads(rd.get(make))
    model_list = []
    for model in make_dict:
        model_list.append(model)

    return jsonify(model_list)


@app.route("/<make>/<model>/data", methods=["GET"])
def model_data(make: str, model: str):
    """
    Gets all data for a specified make and model
    """
    return json.loads(rd.get(make))[model]


@app.route("/<make>/<model>/<feature>")
def get_feature(make: str, model: str, feature: str):
    """
    Gets a feature for a certain make and model
    """
    return f"{feature} for the {model} model of {make} is {json.loads(rd.get(make))[model][feature]}"


@app.route("/average_fuel_consumption_<make>/<type>/<units>", methods=["GET"])
def avg_make_consumption(make:str, type:str, units:str):
    """
    Gets the average fuel consumption of a make of vehicle

    Args:
        make (string) : the make of the vehicle (must be capitalized)
        type (string) : hwy, city, or comb (hwy = highway driving, city = city driving, comb = combined driving)
        units (string) : L or mpg (L/100km or miles per gallon). Note MPG only supports has comb.

    Returns:
        String describing the average fuel consumption

    """

    if units == "mpg":
        index_string = "fuel_consumption(comb_(mpg))"
    else:
        index_string = f"fuel_consumption({type}_(l/100_km))"

    make_dict = json.loads(rd.get(make))
    fuel = []
    for m in make_dict:
        fuel.append(make_dict[m][index_string])

    avg = s.mean(fuel)

    return f"The average {index_string} for {make} is {avg} "


@app.route("/<make>/average_<feature>", methods=["GET"])
def avg_feature(make:str, feature:str):
    """
    Gets the average of any numerical feature
    """
    non_numerical = ["vehicle_class", "transmission", "fuel_type"]
    if feature in non_numerical:
        return "This is a non numerical feature and not able to be averaged "

    feature_sum = []
    make_dict = json.loads(rd.get(make))
    for m in make_dict:
        feature_sum.append(make_dict[m][feature])
    avg = s.mean(feature_sum)

    return f"The average {feature} for {make} is {avg}"


@app.route('/delete/<make>/<model>', methods = ['DELETE'])
def delete_model(make:str, model:str):
    model_dict = json.loads(rd.get(make))
    model_dict.pop(model)
    rd.set(make, json.dumps(model_dict))
    
    return f"{make} {model} deleted from redis database \n"

@app.route('/update/<make>/<model>/<feature>/<value>', methods = ['UPDATE'])
def update(make:str, model:str, feature:str, value):
    model_dict = json.loads(rd.get(make))
    model_dict[model][feature] = value

    rd.set(make, json.dumps(model_dict))

    return f"{make} {model} {feature} updated to {value}"



@app.route('/jobs', methods = ['POST', 'GET'])
def jobs():
    """
    Route to interact with the job. Route accepts a JSON payload describing the job to be created.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['feature1'], job['feature2'], job['comparison']), indent=2) + '\n'

    elif request.method == 'GET':
        redis_dict = {}
        for key in jdb.keys():
            redis_dict[str(key)] = {}
            redis_dict[str(key)]['datetime'] = jdb.hget(key, 'datetime')
            redis_dict[str(key)]['status'] = jdb.hget(key, 'status')
        return json.dumps(redis_dict, indent=4) + '\n' + """
  
  To submit a job, do the following:

  curl localhost:5028/jobs -X POST -d '{"feature1":feature, "feature2":feature, "comparison":comparison}' -H "Content-Type: application/json"
"""

@app.route('/jobs/delete/<job_uuid>', methods=['DELETE'])
def delete_job(job_uuid:str):
    """
    API route to delete a specific job.
    """
    if request.method == 'DELETE':
        if job_uuid == 'all':
            for key in jdb.keys():
                jdb.delete(key)
            return f'All jobs deleted.\n'
        else:
            for key in jdb.keys():
                if key == job_uuid:
                    jdb.delete(key)
        return f'{job_uuid} has been deleted.\n'
    else:
        return """
    This is a route for DELETE-ing former jobs. Use the form:
    curl -X DELETE localhost:5028/jobs/delete/<job>
    Or to delete all jobs, use the form:
    curl -X DELETE localhost:5028/jobs/delete/all
    """ 

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid: str):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'  


@app.route("/interact", methods=["GET"])
def interact():
    """
    Outputs information on how to interact with the application.

    Returns:
        ret (string): how to interact with the application
    """
    logging.info("How to interact with application")

    ret = "How to interact with the application:\n"
    ret += "curl localhost:<port number>/interact                           (GET) prints this infromation\n"
    ret += "curl localhost:<port number>/load_data -X POST                  (POST) reads in the fuel consumption data\n"
    return ret


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
