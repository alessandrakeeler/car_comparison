# Insert quirky title here for pity points 
### By Alessandra Keeler, Gauri Nukula, and Sydney Loats 
#




## **The Data**     
See the orginal source of the data [here](https://www.kaggle.com/datasets/rinichristy/2022-fuel-consumption-ratings). Instructions for downloading the data can be foind in the "getting started" section. 


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
- *gitignore*
- *README.me*



### **/src**  
- *app.py*  
        This is the main file for the API. 
- *workers.py* 
- *jobs.py*

### /docker
- *Dockerfile.api*
- *Dockerfile.wrk*



### /kubernetes 



### /test
- *test_flask.py*




## **Getting Started with the Repo**
## **Interacting with the API**


## **Citations**




