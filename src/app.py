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
    global col

    df = pd.read_csv('MY2022 Fuel Consumption Ratings.csv')

    col = df.drop(['Make', 'Model'], axis = 1).columns

    for make in df['Make'].unique(): 
        out = { make: df.loc[df['Make'] == make].groupby('Model')[col].last().to_dict(orient='index')}
        if make == 'Acura' : 
            data = {'Make': out}
        else:
            data['Make'][make] = out[make]

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
    make_list = [make for make in data['Make']]
    return jsonify(make_list)

@app.route('/arguments', methods = ['GET'])
def get_arguments():
    """
    Ouputs all possible arguments for each make
    """
    return jsonify(col)

@app.route('/<make>', methods=['GET'])
def models_for_make(make):
    """
    Outputs all models under a specified make. Make must be capitalized. 

    """

    make_dict = data['Make'][make]
    model_list = []
    for model in make_dict:
        model_list.append(model)

    return jsonify(model_list)

@app.route('/<make>/<model>', methods = ['GET'])
def model_data(make, model):
    """
    Gets all data for a specified make and model
    """
    return data['Make'][make][model]


@app.route('/average_fuel_consumption_<make>/<type>/<units>')
def avg_make_consumption(make, type, units):
    """
    Gets the average fuel consumption of a make of vehicle

    Args:
        make (string) : the make of the vehicle (must be capitalized)
        type (string) : Hwy, City, or Comb (hwy = highway driving, city = city driving, comb = combined driving)
        units (string) : L or mpg (L/100km or miles per gallon)

    Returns: 
        String describing the average fuel consumption 
  
    """

    if units == 'mpg':
        index_string = "Fuel Consumption(Comb (mpg))"
    else:
        index_string = f"Fuel Consumption({type} (L/100 km))"

    fuel = []
    for m in data['Make'][make]:
        fuel.append(data['Make']['Acura'][m][index_string])
        
    avg = s.mean(fuel)

    return f"The average {index_string} for {make} is {avg} "






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
