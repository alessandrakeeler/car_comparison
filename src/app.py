from flask import Flask, jsonify
import logging
import xmltodict
import pandas as pd
import json 

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



@app.route('/makes', methods = ['GET'])
def get_makes():
    """
    Outputs all makes in dataset.
    """
    make_list = [make for make in data['Make']]
    return jsonify(make_list)


@app.route('/models_for_<make>', methods=['GET'])
def models_for_make(make):
    """
    Outputs all models under a specified make. Make must be capitalized. 

    """

    make_dict = data['Make'][make]
    model_list = []
    for model in make_dict:
        model_list.append(model)


    return jsonify(model_list)




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
