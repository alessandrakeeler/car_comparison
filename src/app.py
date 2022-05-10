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

""" redis_ip = os.environ.get('REDIS_IP')
if not redis_ip:
    raise Exception() """

rd = redis.StrictRedis(host="127.0.0.1", port=6413, db=13)


app = Flask(__name__)


@app.route("/data", methods=["POST", "GET"])
def load_data():
    """
    Loads fuel consumption data.

    Returns:
        string that states that the data has been loaded.
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

        return "Data loaded into redis"

    elif request.method == "GET":
        makes = []
        for item in rd.keys():
            makes.append({item.decode("utf-8"): json.loads(rd.get(item))})
        return json.dumps(makes, indent=4)

    else:
        return "Method only supports POST and GET"


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
    Ouputs all possible features for each make
    """
    feature_list = list(json.loads(rd.get(make))[model].keys())
    return jsonify(feature_list)


@app.route("/<make>", methods=["GET"])
def models_for_make(make):
    """
    Outputs all models under a specified make.

    """
    make_dict = json.loads(rd.get(make))
    model_list = []
    for model in make_dict:
        model_list.append(model)

    return jsonify(model_list)


@app.route("/<make>/<model>/data", methods=["GET"])
def model_data(make, model):
    """
    Gets all data for a specified make and model
    """
    return json.loads(rd.get(make))[model]


@app.route("/<make>/<model>/<feature>")
def get_feature(make, model, feature):
    """
    Gets a feature for a certain make and model
    """
    return f"{feature} for the {model} model of {make} is {json.loads(rd.get(make))[model][feature]}"


@app.route("/average_fuel_consumption_<make>/<type>/<units>", methods=["GET"])
def avg_make_consumption(make, type, units):
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
def avg_feature(make, feature):
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


@app.route("/scatter/<feature1>/<feature2>", methods=["GET"])
def scatter_feature_make(feature1, feature2):
    """
    Scatterplots two features against eachother, compared on make
    """

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

    ## TODO figure out how to make less horrifically inneficient
    df = pd.DataFrame(columns=features)
    for key in rd.keys():
        make_dict = json.loads(rd.get(key))
        for model in make_dict:
            list_items = list((make_dict[model]).items())
            data_list = [item[1] for item in list_items]
            df = df.append(pd.Series(data_list, index=df.columns), ignore_index=True)

    sns.set(rc={"figure.figsize": (11.7, 8.27)})
    scatter = sns.scatterplot(data=df, x=feature1, y=feature2, hue="make")

    fig = scatter.get_figure()
    plt.legend(fontsize="small", loc=2, bbox_to_anchor=(1, 1.16))
    fig.savefig(f"{feature1}_vs_{feature2}.png")
    return "Graph saved \n"


@app.route("/scatter/<feature1>/<feature2>/<comparison>", methods=["GET"])
def scatter_feature_comparison(feature1, feature2, comparison):
    """
    Scatterplots two numerical features, compared on a custom categorical feature
    """
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

    categorical_features = [
        "make",
        "model",
        "vehicle_class",
        "transmission",
        "fuel_type",
    ]
    if comparison not in categorical_features:
        return "Sorry, this is a numerical feature! Please pick a categorical feature as the comparison factor \n"

    df = pd.DataFrame(columns=features)
    for key in rd.keys():
        make_dict = json.loads(rd.get(key))
        for model in make_dict:
            list_items = list((make_dict[model]).items())
            data_list = [item[1] for item in list_items]
            df = df.append(pd.Series(data_list, index=df.columns), ignore_index=True)

    sns.set(rc={"figure.figsize": (11.7, 8.27)})
    scatter = sns.scatterplot(data=df, x=feature1, y=feature2, hue=comparison)
    fig = scatter.get_figure()
    plt.legend(fontsize="small", loc=2)
    fig.savefig(f"{feature1}_vs_{feature2}_compared_on_{comparison}.png")
    return "Graph saved \n"


@app.route('/delete/<make>/<model>', methods = ['DELETE'])
def delete_model(make, model):
    model_dict = json.loads(rd.get(make))
    model_dict.pop(model)
    rd.set(make, json.dumps(model_dict))
    
    return f"{make} {model} deleted from redis database \n"

@app.route('/update/<make>/<model>/<feature>/<value>', methods = ['UPDATE'])
def update(make, model, feature, value):
    model_dict = json.loads(rd.get(make))
    model_dict[model][feature] = value

    rd.set(make, json.dumps(model_dict))

    return f"{make} {model} {feature} updated to {value}"





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
