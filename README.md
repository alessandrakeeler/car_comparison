# Car shopping? Beating your competitors? Imaginging you can afford an Aston Martin? Why not all! 
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

## **Getting Started with the Repo**
The initial setup of this repository is fairly simple! 
Run  `git clone git@github.com:alessandrakeeler/car_comparison.git`   
Steps to download the data:
1. Download the data from [this](https://www.kaggle.com/datasets/rinichristy/2022-fuel-consumption-ratings?resource=download&select=MY2022+Fuel+Consumption+Ratings.csv) link. The data wil download as a zip. 
2. Click the zip in downloads to open it. Rename the .csv file inside to fuel_ratings.csv
3. Use whatever method you prefer to scp the data from local to remote.
4. Place fuel_ratings.csv into the root of the car_comparison directory. 

Now, we need to set up the Flask/Redis environments to run this project in.   
Run `make all`, if it succeeded, you should get a message along the lines of `"successfully built"`


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








## **Interacting with the API (CRUD)**   
The API has a wide variety of routes for investigating the data set.   
All route commands start with `curl localhost:<port number>/<route_to_execute> `   
Ex): `curl localhost:5000/makes`   

Before any data querying routes can be ran, the data must first be read into the Redis database. To do this, run `curl localhost<port_number>/data -X POST`   
If the data load was successful, the output is "Data loaded into Redis".  
Troubleshooting the data upload:
- Make sure that the data file is named fuel_ratings.csv and in the root directory.   


The routes within this API (to execute, need to start the command with `curl localhost:<port number>/`):

- ` /interact ` prints the information about each route and how to call them 
- ` /data -X POST ` reads fuel consumption data into redis database
- ` /data -X GET ` returns all fuel consumption data in dictionary form
- ` /makes `  returns all car makes in the dataset
- ` /<make>/models` returns all models for a given make
- `/<make>/<model>/features `returns all features (without actual data) of a given make and model
- `/<make>/<model>/data `  returns all data associated with a given make and model
- `/<make>/<model>/<feature>  `  returns the value of a specified feature for a specified make and model 
- `/average_fuel_consumption_<make>/<type>/<units>  ` returns the average fuel consumption for a make of specified type (hwy, city, comb) for specified units (L or mpg) 
-  `/<make>/average_<feature>   ` returns average of a specified feature for a specified make
-  `/delete/<make>/<model> -X DELETE ` deletes a specified make and model from the redis database 
- `/update/<make>/<model>/<feature>/<value> -X UPDATE` updates a specified feature of specified make and model to new given value 

### Some sample output of CRUD Jobs:   

` curl localhost:<portnumber>/makes`  

[
  "mini", 
  "cadillac", 
  "jeep", 
  "maserati", 
  "audi", 
  "porsche", 
  "lincoln", 
  "mercedes-benz", 
  "genesis", 
  "volkswagen", 
  "alfa_romeo", 
  "ram", 
  "dodge", 
  "lamborghini", 
  "ford", 
  "bmw", 
  "hyundai", 
  "land_rover", 
  "nissan", 
  "honda", 
  "buick", 
  "mazda", 
  "lexus", 
  "jaguar", 
  "subaru", 
  "acura", 
  "fiat", 
  "kia", 
  "toyota", 
  "chrysler", 
  "bentley", 
  "volvo", 
  "bugatti", 
  "rolls-royce", 
  "mitsubishi", 
  "chevrolet", 
  "aston_martin", 
  "infiniti", 
  "gmc"
]


`curl localhost:<port_number>/acura/ilx/data`  
{
  "co2_emissions(g/km)": 200, 
  "co2_rating": 6, 
  "cylinders": 4, 
  "engine_size(l)": 2.4, 
  "fuel_consumption(comb_(l/100_km))": 8.6, 
  "fuel_consumption(comb_(mpg))": 33, 
  "fuel_consumption(hwy_(l/100_km))": 7.0, 
  "fuel_consumption_(city_(l/100_km)": 9.9, 
  "fuel_type": "z", 
  "make": "acura", 
  "model": "ilx", 
  "smog_rating": 3, 
  "transmission": "am8", 
  "vehicle_class": "compact"
}


    




## **Interacting with the API (Jobs)**
- `/jobs -X GET   `   will return instructions on how to submit a job
- `/jobs/delete/<job_uuid> -X DELETE `  will delete a job given the job uuid 
- ` /jobs/<job_uuid>     `  checks the status of a submitted job 
- `/download/<job_uuid> `   downloads the image generated by the worker

## **Citations**




