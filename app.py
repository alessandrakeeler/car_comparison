from flask import Flask
import logging
import xmltodict

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

    with open('MY2022_Fuel_Consumption_Ratings.xml', 'r') as f:
   # with open('test.xml', 'r') as f:
        data = xmltodict.parse(f.read())

    return f'Data loaded from file to dictionary.\n'



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


@app.route('/print', methods=['GET'])
def print():

#    for i in range(len(data['Workbook']['Worksheet']['Table']['Row'])):
    ret_dict = {}
 
    ret_dict['Model Year'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][0]['Data']
    ret_dict['Make']= data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][1]['Data']
    ret_dict['Model'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][2]['Data']
    ret_dict['Vehicle Class'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][3]['Data']
    ret_dict['Engine Size(L)'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][4]['Data']
    ret_dict['Cylinders'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][5]['Data']
    ret_dict['Transmission'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][6]['Data']
    ret_dict['Fuel Type'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][7]['Data']
    ret_dict['Fuel Consumption (City (L/100 km)'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][8]['Data']
    ret_dict['Fuel Consumption(Hwy (L/100 km))'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][9]['Data']
    ret_dict['Fuel Consumption(Comb (L/100 km))'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][10]['Data']
    ret_dict['Fuel Consumption(Comb (mpg))'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][11]['Data']
    ret_dict['CO2 Emissions(g/km)'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][12]['Data']
    ret_dict['CO2 Rating']=data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][13]['Data']
    ret_dict['Smog Rating'] = data['Workbook']['Worksheet']['Table']['Row'][1]['Cell'][14]['Data']

   # ret_dict['Make']=data['Table']['Cell'][1]['Data']
   # ret_dict['Model']=data['Table']['Cell'][2]['Data']
  #  ret_dict['Vehicle Class']=data['Table']['Cell'][3]['Data']
 #   ret_dict['Engine Size(L)']=data['Table']['Cell'][4]['Data']
   # ret_dict['Cylinders']=data['Table']['Cell'][5]['Data']
  #  ret_dict['Transmission']=data['Table']['Cell'][6]['Data']
 #   ret_dict['Fuel Type']=data['Table']['Cell'][7]['Data']
    return ret_dict




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
