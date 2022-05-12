# The Biggest Offenders of the Road (And Wallets!!) of 2022
### By Alessandra Keeler, Gauri Nukala, and Sydney Loats 
#
This project was developed to investigate the differences between cars produced in 2022. More specifically, their fuel consumption and impact on the enviroment (through emissions, smog rating, etc.) Whether this is used by manufactorers to see how their products stand up against competitors or consumers determining which vehicle is the best purchase, it presents a large amount of data in an easily accessible manner. Feel free to play around and compare car makes, models, vehicle classes, and many many more features to eachother!   





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

Some important definitions/clarifications: 
- make is what you think of when you think car "brand". Acura, Toyota, Volvo, are all MAKES
- model is the "style" of car that falls under the "brand". ILX and MDX SH-AWD are MODELS of the MAKE Acura. 
- All data in this dataset is lowercase, and all spaces are replaced with underscores. (See example below)
- "Feature" refers to the datapoints within each car (ie smog_rating, fuel_type, etc...)
- Each car is identified through both its make and model. 

The data is stored in a Redis database, its structure resembles the folowing JSON: 
```
Note that there are obviously more vehicle models per each make, however the data was truncated for readability. 
       "infiniti": {
            "q50_awd": {
                "make": "infiniti",
                "model": "q50_awd",
                "vehicle_class": "mid-size",
                "engine_size(l)": 3.0,
                "cylinders": 6,
                "transmission": "as7",
                "fuel_type": "z",
                "fuel_consumption_(city_(l/100_km)": 12.5,
                "fuel_consumption(hwy_(l/100_km))": 8.7,
                "fuel_consumption(comb_(l/100_km))": 10.8,
                "fuel_consumption(comb_(mpg))": 26,
                "co2_emissions(g/km)": 254,
                "co2_rating": 5,
                "smog_rating": 3
            },
            "qx80_4wd": {
                "make": "infiniti",
                "model": "qx80_4wd",
                "vehicle_class": "suv:_standard",
                "engine_size(l)": 5.6,
                "cylinders": 8,
                "transmission": "as7",
                "fuel_type": "z",
                "fuel_consumption_(city_(l/100_km)": 17.5,
                "fuel_consumption(hwy_(l/100_km))": 12.2,
                "fuel_consumption(comb_(l/100_km))": 15.1,
                "fuel_consumption(comb_(mpg))": 19,
                "co2_emissions(g/km)": 355,
                "co2_rating": 3,
                "smog_rating": 3
            }, ...
        }
    ,
    {
        "gmc": {
            "acadia": {
                "make": "gmc",
                "model": "acadia",
                "vehicle_class": "suv:_standard",
                "engine_size(l)": 3.6,
                "cylinders": 6,
                "transmission": "a9",
                "fuel_type": "x",
                "fuel_consumption_(city_(l/100_km)": 12.3,
                "fuel_consumption(hwy_(l/100_km))": 8.8,
                "fuel_consumption(comb_(l/100_km))": 10.7,
                "fuel_consumption(comb_(mpg))": 26,
                "co2_emissions(g/km)": 252,
                "co2_rating": 5,
                "smog_rating": 6
            },...
            }
```

## **Getting Started with the Repo**
The initial setup of this repository is fairly simple! 
Run  `git clone git@github.com:alessandrakeeler/car_comparison.git` in whatever location you want to run this application from.   
Steps to download the data:
1. Download the data from [this](https://www.kaggle.com/datasets/rinichristy/2022-fuel-consumption-ratings?resource=download&select=MY2022+Fuel+Consumption+Ratings.csv) link. The data wil download as a zip. 
2. Click the zip in downloads to open it. Rename the .csv file inside to fuel_ratings.csv
3. Use whatever method you prefer to scp the data from local to remote, if necessary. 
4. Place fuel_ratings.csv into the root of the car_comparison directory. 

**Only do the next steps if you don't already have Kubernetes pods already running for this project!!**
 
Run `make all`, to build the Docker images necessary for this deployment. if it succeeded, you should get a message along the lines of `"successfully built"`
Run `push-all` to push to the DockerHub
Log into isp `ssh <user>@isp.tacc.utexas.edu` then into `ssh <username>@coe332-k8s.tacc.cloud`
Now run the below commands in order. 
```
kubectl apply -f app-prod-db-service.yml
kubectl apply -f app-prod-db-pvc.yml
kubectl apply -f app-prod-db-deployment.yml
```
Next, run `kubectl get services` and copy the cluster_ip.   
Paste the cluser_ip under the value of REDIS_IP in *app-prod-api-development.yaml* and *app-prod-wrk-development.yaml*.  
Now, execute the following commands on K8s. 
```
kubectl apply -f app-prod-api-service.yml
kubectl apply -f app-prod-api-deployment.yml
kubectl apply -f app-prod-wrk-deployment.yml
```

Make sure all your pods are running by using the command `kubectl get all -o wide`

To start using the API, execute into the debug pod by running `kubectl exec -it <pod_name> /bin/bash.  
See below for routes to curl. 

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
- *app-prod-api-deployment.yml*
- *app-prod-api-service.yml*
- *app-prod-db-deployment.yml*
- *app-prod-db-pvc.yml*
- *app-prod-db-service.yml*
- *app-prod-wrk-deployment.yml*



### /test
- *test_flask.py*   
This is the file where all of the API tests are contained. 








## **Interacting with the API (CRUD)**   
The API has a wide variety of routes for investigating the data set.   
The API depends on the IP Address of the API service, run `kubectl get services` and copy the cluster_ip for the api service. In the case of this app, it is `10.110.170.141`.    

All route commands start with `curl <api_ip>:5000/<route_to_execute> ` while inside the api-deployment pod (see above for instructions on that!).    
Ex): `curl 10.110.170.141:5000/makes`   

Before any data querying routes can be ran, the data must first be read into the Redis database. To do this, run `curl <api_ip>:<port_number>/data -X POST`   
If the data load was successful, the output is "Data loaded into Redis".  
Troubleshooting the data upload:
- Make sure that the data file is named fuel_ratings.csv and in the root directory before building and pushing docker images.   


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

` curl 10.110.170.141:5000/makes`  

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


`curl 10.110.170.141:5000/acura/ilx/data`  
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
- `/jobs -X POST -d '{"feature1":feature1, "feature2":feature2, "comparison_factor":comparison_factor}' -H "Content-Type: application/json" ` will create a job and return the job id
- `/jobs/delete/<job_uuid> -X DELETE `  will delete a job given the job uuid 
- ` /jobs/<job_uuid>     `  checks the status of a submitted job 
- `/download/<job_uuid> `   downloads the image generated by the worker   

Sample job done by the graphing worker:   
![sample_image](https://github.com/alessandrakeeler/car_comparison/blob/main/sample_image.png?raw=true)

## **Citations**

Rimi. 2022 Fuel Consumption Ratings. Kaggle. Retrieved April 10, 2022, from https://www.kaggle.com/datasets/rinichristy/2022-fuel-consumption-ratings?resource=download&select=MY2022+Fuel+Consumption+Ratings.csv



