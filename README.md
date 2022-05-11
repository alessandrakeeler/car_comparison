# Insert quirky title here for pity points 
### By Alessandra Keeler, Gauri Nukula, and Sydney Loats 
#
This project was developed to investigate the differences between cars produced in 2022. Whether this is used by manufactorers to see how their products stand up against competitors or consumers determining which vehicle is the best purchase, it presents a large amount of data in an easily accessible manner. Feel free to play around and compare car makes, models, vehicle classes, and many many more features to eachother!   





## **The Data**     
See the orginal source of the data [here](https://www.kaggle.com/datasets/rinichristy/2022-fuel-consumption-ratings). Instructions for downloading the data can be found in the "getting started" section. 


This data describes all vehicles released in 2022. It includes the following features:

- make 
- model
- vehicle_class
- engine_size(l)
- cylinders
- transmission
- fuel_type
- fuel_consumption_(city_(l/100_km)
- fuel_consumption(hwy_(l/100_km))
- fuel_consumption(comb_(l/100_km))
- fuel_consumption(comb_(mpg))
- co2_emissions(g/km)
- co2_rating
- smog_rating

The data is stored in a Redis database, its structure resembles the folowing JSON: 
```
Note that there are obviously more vehicle models per each make, however the data was truncated for readability. 
"Acura": {
            "ILX": {
                "Vehicle Class": "Compact",
                "Engine Size(L)": 2.4,
                "Cylinders": 4,
                "Transmission": "AM8",
                "Fuel Type": "Z",
                "Fuel Consumption (City (L/100 km)": 9.9,
                "Fuel Consumption(Hwy (L/100 km))": 7.0,
                "Fuel Consumption(Comb (L/100 km))": 8.6,
                "Fuel Consumption(Comb (mpg))": 33,
                "CO2 Emissions(g/km)": 200,
                "CO2 Rating": 6,
                "Smog Rating": 3
            }
        }, ... }
"Alfa Romeo": {
            "Giulia": {
                "Vehicle Class": "Mid-size",
                "Engine Size(L)": 2.0,
                "Cylinders": 4,
                "Transmission": "A8",
                "Fuel Type": "Z",
                "Fuel Consumption (City (L/100 km)": 10.0,
                "Fuel Consumption(Hwy (L/100 km))": 7.2,
                "Fuel Consumption(Comb (L/100 km))": 8.7,
                "Fuel Consumption(Comb (mpg))": 32,
                "CO2 Emissions(g/km)": 205,
                "CO2 Rating": 6,
                "Smog Rating": 3
            }, ... }
            }
        

```


## **Files**
### **root**
- *requirements.txt*   
This file contains the required Python packages necessary to run the API
- *gitignore*   
All file extensions to be excluded (for development purposes)
- *README.me*   
The document you're reading now. Oh hey! Funny seeing you here. 



### **/src**  
- *app.py*  
        This is the main file for the API. See below for descriptions of all routes within this file. 
- *workers.py*   
This file contains the function for the graphing worker. It utilizes functions from jobs.py to preform queued jobs. 
- *jobs.py*   
This file contains all job related functions (save, update, etc.). These functions are called in app.py as a part of various routes. 

### /docker
- *Dockerfile.api*   
This is the Dockerfile that builds the image and all dependencies to run the Flask API
- *Dockerfile.wrk*   
This is the Dockerfile that builds the image and all dependencies for workers. 



### /kubernetes 



### /test
- *test_flask.py*   
This is the file where all of the API tests are contained. 




## **Getting Started with the Repo**
## **Interacting with the API (CRUD)**   
The API has a wide variety of routes for investigating the data set.   
All route commands start with `curl localhost:<port number>/<route_to_execute> `   
Ex): `curl localhost:5000/makes`   


The routes within this API:




## **Interacting with the API (Jobs)**

## **Citations**




