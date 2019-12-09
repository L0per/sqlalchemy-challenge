# SQLAlchemy Climate Analysis and Flask API Development
* Using provided `.sqlite` and `.csv` files containing weather data from various Hawaii weather stations, the weather data is analyzed and an API is developed to assist in planning a fictional trip:

  1. **Weather Analysis**: Using SQLAlchemy, the SQLite database is queried and analyzed using Pandas and Matplotlib.
  2. **API Development**: Using Flask and the SQLite database, an API is created for various queries.

## Files
* `climate.ipynb` = Jupyter notebook for weather analysis
* `app.py` = Flask API for querying Hawaii weather stations
* [data](https://github.com/L0per/sqlalchemy_flask_api_tripweather/tree/master/Data) =SQLite database and `.csv` files

## Weather Analysis
* The last year of `.sqlite` precipitation data was queried into Pandas and plotted:

![prec_plot](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/prcp_year.png?raw=true)

* Using the most active temperature reading station data (Waihee), the last year of temperature data was plotted as a histogram:

![waihee_plot](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/temp_waihee_year.png?raw=true)

## Trip Weather Analysis
* For a fictionally planned trip to Hawaii from 05-20-2018 to 05-30-2018, the weather was analyzed for historical trends within this date range.

### June vs. December Temperature
* `.csv` files of the database were loaded into pandas and the average temperatures for all June and Decemeber readings were averaged:

![avg_temps](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/avg_temps.PNG?raw=true)

* To find whether there was a statistically significant difference between the temperature averages, all of June and December data was analyzed by a Levene and independent t-test:

![ttest](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/ttest.PNG?raw=true)

* Unpaired (independent) t-test used due to Levene test showing unequal variances.
  * Addtionally, there are not the same number of data points and the data can be from different stations.
* The mean temperature difference between June and December **is statistically significant**.

### Temperature During Planned Trip
* Using the trip date range for the previous year (05-20-2017 to 05-30-2017), the average/min/max temperature was plotted:

![trip_temp_avg](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/temp_avg_trip.png?raw=true)

* Using all historical data, the temperature normals (average/min/max) were plotted for each day of the planned trip:

![trip_temp_avg](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/trip_normals.png?raw=true)

## Weather API
* An API was created with various routes for querying the weather SQLite database:

![API](https://github.com/L0per/sqlalchemy_flask_api_tripweather/blob/master/Images/API.PNG?raw=true)
