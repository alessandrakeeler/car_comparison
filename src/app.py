from flask import Flask, jsonify, request
import logging
import pandas as pd
import json
import statistics as s
import os
import redis
import seaborn as sns
import matplotlib.pyplot as plt
#from helper_functions import make_exists, model_exists --deprecated
from jobs import *


app = Flask(__name__)

@app.route("/interact", methods=["GET"])
def interact():
    """
    Outputs information on how to interact with the application.
    Args: None
    Returns:
        ret (string): how to interact with the application
    """
    logging.info("How to interact with application")

    ret = "How to interact with the application:\n"
    ret += "curl localhost:<port number>/interact                           (GET) prints this information\n"
    ret += "curl localhost:<port number>/data -X POST                       (POST) reads fuel consumption data into redis database\n"
    ret += "curl localhost:<port number>/data -X GET                        (GET) returns all fuel consumption data in dictionary form\n"
    ret += "curl localhost:<port number>/makes                              (GET) returns all car makes in the dataset\n"
    ret += "curl localhost:<port number>/<make>/models                      (GET) returns all models for a given make\n"
    ret += "curl localhost:<port number>/<make>/<model>/features            (GET) returns all features of a given make and model (possible data points)\n"
    ret += "curl localhost:<port number>/<make>/<model>/data                (GET) returns all data associated with a given make and model\n"
    ret += "curl localhost:<port number>/<make>/<model>/<feature>           (GET) returns the value of a specified feature for a specified make and model \n"
    ret += "curl localhost:<port number>/average_fuel_consumption_<make>/<type>/<units>    (GET) returns the average fuel consumption for a make of specified type (hwy, city, comb) for specified units (L or mpg) \n"
    ret += "curl localhost:<port number>/<make>/average_<feature>           (GET) returns average of a specified feature for a specified make \n"
    ret += "curl localhost:<port number>/delete/<make>/<model> -X DELETE    (DELETE) deletes a specified make and model from the redis database \n"
    ret += "curl localhost:<port number>/update/<make>/<model>/<feature>/<value> -X UPDATE  (UPDATE) updates a specified feature of specified make and model to new given value \n"
    ret += "curl localhost:<port number>/jobs -X GET                        (GET) will return instructions on how to submit a job \n"
    ret += "curl localhost:<port number>/jobs/delete/<job_uuid> -X DELETE   (DELETE) will delete a job given the job uuid \n"
    ret += "curl localhost:<port number>/jobs/<job_uuid>                    (GET) checks the status of a submitted job \n"
    ret += "curl localhost:<port number>/download/<job_uuid>                (GET) downloads the image generated by the worker \n"
    
    return ret

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
    Iterates through keys in redis database (makes)
    Args: None
    Returns:
        Jsonified list of all makes in the dataset
    """
    make_list = []
    for key in rd.keys():
        make_list.append(key.decode("utf-8"))
    return jsonify(make_list)

@app.route("/<make>/models", methods=["GET"])
def models_for_make(make: str):
    """
    Outputs all models under a specified make.
    Args: make (string)
    Returns: jsonified list of all models under a specified make
    """

    make_dict = json.loads(rd.get(make))
    model_list = []
    for model in make_dict:
        model_list.append(model)

    return jsonify(model_list)


@app.route("/<make>/<model>/features", methods=["GET"])
def get_arguments(make, model):
    """
    Ouputs all possible features for each make and model
    Args: 
        make (string)
        model (string)
    Returns: 
        jsonified list of all features for specified make and model 
    """

    make_dict = json.loads(rd.get(make))
    return jsonify(list(make_dict[model].keys()))


@app.route("/<make>/<model>/data", methods=["GET"])
def model_data(make: str, model: str):
    """
    Outputs all data associated with a specified make and model 
    Args:
        make (string)
        model (string)
    Returns:
        Dictionary of all data 
    """
    return json.loads(rd.get(make))[model]


@app.route("/<make>/<model>/<feature>")
def get_feature(make: str, model: str, feature: str):
    """
    Gets a feature for a certain make and model
    Args:
        make (string)
        model (string)
        feature (string)
    Returns: 
        String describing the feature. 
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
    Gets the average of any numerical feature for a given make 
    Args:
        make(string)
        feature(string)
    Returns:
        A string describing the average of the specified feature for the specified make 
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
    """
    Deletes a make/model entry 
    Args:
        make(string)
        model(string)
    Returns: 
        A string describing the car that was deleted from the Redis database 
    """
    model_dict = json.loads(rd.get(make))
    model_dict.pop(model)
    rd.set(make, json.dumps(model_dict))
    
    return f"{make} {model} deleted from redis database \n"

@app.route('/update/<make>/<model>/<feature>/<value>', methods = ['UPDATE'])
def update(make:str, model:str, feature:str, value):
    """
    Update a feature for a specified car in the Redis database 
    Args: 
        make(string)
        model(string)
        feature(string)
        value(int or string): int if updating a numerical feature, string if updating a categorical feature. 
    """

    model_dict = json.loads(rd.get(make))
    model_dict[model][feature] = value

    rd.set(make, json.dumps(model_dict))

    return f"{make} {model} {feature} updated to {value}"



@app.route('/jobs', methods = ['POST', 'GET'])
def jobs():
    """
    Route to interact with the job. Route accepts a JSON payload describing the job to be created.
    POST: Add a job to the database 
    GET: Returns the command to add a job to the database 
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['feature1'], job['feature2'], job['comparison_factor']), indent=2) + '\n'

    elif request.method == 'GET':
        redis_dict = {}
        for key in jdb.keys():
            redis_dict[str(key)] = {}
            redis_dict[str(key)]['datetime'] = jdb.hget(key, 'datetime')
            redis_dict[str(key)]['status'] = jdb.hget(key, 'status')
        return json.dumps(redis_dict, indent=4) + '\n' + """
  
  To submit a job, do the following:

  curl localhost:5000/jobs -X POST -d '{"feature1":"feature", "feature2":"feature", "comparison_factor":"comparison"}' -H "Content-Type: application/json"
"""

@app.route('/jobs/delete/<job_uuid>', methods=['DELETE'])
def delete_job(job_uuid:str):
    """
    Deletes a job from the job. 
    Args:
        job_uuid(string): uuid of job to be deleted
    Returns:
        String confirming job has been deleted
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
    Args: 
        job_uuid(string): uuid of job to be status checked 
    Returns:
        Dictionary describing the status of the requested jj_uuid

    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'  

# download image route 
@app.route('/download/<job_uuid>', methods=['GET'])
def download(job_uuid):
    """
    Downloads the image associated with the specified job_uuid
    Args:
        job_uuid(string): uuid of job to be downloaded
    Returns:
        file to be downloaded as attachment 
    """
    path = f'/app/{job_uuid}.png'
    with open(path, 'wb') as f:
        f.write(img_db.hget(f'job.{job_uuid}', 'image'))
    return send_file(path, mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


