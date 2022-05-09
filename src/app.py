from flask import Flask, jsonify
import logging
import xmltodict
import pandas as pd
import json 
import statistics as s 

app = Flask(__name__)

data = {}

@app.route('/load_data', methods=['POST'])
def load_data():
    """
    Loads fuel consumption data.

    Returns:
        string that states that the data has been loaded.
    """
    logging.info('Reading in fuel consumption data.')

    global data

    df = pd.read_csv('MY2022 Fuel Consumption Ratings.csv')
    columns = [c.replace(' ', '_').lower() for c in list(df.columns)]
    col = [columns[i] for i in range(1, len(columns))]
    df.columns = columns

    for make in df['make'].unique(): 
        out = { make: df.loc[df['make'] == make].groupby('model')[col].last().to_dict(orient='index')}
        if make == 'Acura' : 
            data = {'make': out}
        else:
            data['make'][make] = out[make]

    return f'Data loaded from file to dictionary.\n'


@app.route('/print_data', methods = ['GET'])
def print_data():
    json_obj = json.dumps(data, indent = 4)
    return json_obj


@app.route('/makes', methods = ['GET'])
def get_makes():
    """
    Outputs all makes in dataset.
    """
    make_list = [make for make in data['make']]
    return jsonify(make_list)

@app.route('/<make>/<model>/features', methods = ['GET'])
def get_arguments(make, model):
    """
    Ouputs all possible features for each make
    """
    return jsonify(list(data['make'][make][model].keys()))

@app.route('/<make>', methods=['GET'])
def models_for_make(make):
    """
    Outputs all models under a specified make. make must be capitalized. 

    """

    make_dict = data['make'][make]
    model_list = []
    for model in make_dict:
        model_list.append(model)

    return jsonify(model_list)

@app.route('/<make>/<model>', methods = ['GET'])
def model_data(make, model):
    """
    Gets all data for a specified make and model
    """
    return data['make'][make][model]

@app.route('/<make>/<model>/<feature>')
def get_feature(make, model, feature):
    """
    Gets a feature for a certain make and model
    """
    return f"{feature} for the {model} model of {make} is {data['make'][make][model][feature]}"


@app.route('/average_fuel_consumption_<make>/<type>/<units>')
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

    if units == 'mpg':
        index_string = "fuel_consumption(comb_(mpg))"
    else:
        index_string = f"fuel_consumption({type}_(l/100_km))"

    fuel = []
    for m in data['make'][make]:
        fuel.append(data['make'][make][m][index_string])
        
    avg = s.mean(fuel)

    return f"The average {index_string} for {make} is {avg} "


@app.route('/<make>/average_<feature>')
def avg_feature(make, feature):
    """ 
    Gets the average of any numerical feature
    """
    non_numerical = ["vehicle_class", "transmission", "fuel_type"]
    if feature in non_numerical:
        return "This is a non numerical feature and not able to be averaged "

    feature_sum = []
    for m in data['make'][make]:
        feature_sum.append(data['make'][make][m][feature])
    avg = s.mean(feature_sum)

    return f"The average {feature} for {make} is {avg}"


















@app.route('/interact', methods=['GET'])
def interact():
    """
    Outputs information on how to interact with the application.

    Returns:
        ret (string): how to interact with the application
    """
    logging.info('How to interact with application')

    ret = "How to interact with the application:\n"
    ret+= "curl localhost:<port number>/interact                           (GET) prints this infromation\n"
    ret+= "curl localhost:<port number>/load_data -X POST                  (POST) reads in the fuel consumption data\n"
    return ret;

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
