# `CZ_2010` API Development (July 13, 2019)

This code represents a minimal viable product (MVP) that can be elaborated to develop a production API that can be used for the CZ_2010, or newer, weather datasets.  These `CZ_2010` datasets are used in meter-based energy efficiency calculations, among other uses. 

Right now, this API only contains the weather data for three stations in Southern California.

* BURBANK-GLENDALE, 722880 
* LONG-BEACH, 722970 
* LOS-ANGELES-DOWNTOWN, 722874

For each of these stations, you are able to request the entire years’ worth (i.e., 12 months, or 365 days) of CZ_2010 typical year weather data.

The base address for the connection string used by this API is:

 ```
 https://cz-2010-api.herokuapp.com/
 ```

Keep in mind that this API is an MVP that can be used as a proof-of-concept when developing and maintaining this dataset. That being said, the best route to illistrate the utility of this API is provided below. This route takes in the station number, and a month start and month end date and will return all of the data for that station for the timeframe between those two months.

```
/api/v1.0/<station>/<start_date>/<end_date>
```

For example, if the route called is `/api/v1.0/722874/01/03` then all of the data from the Los Angeles, Downtown station will be retrieved for the months of Jan, Feb and Mar. The full connection string for this API call would be:

```
https://cz-2010-api.herokuapp.com/api/v1.0/722874/01/03
```

The data that is being sent back from the API will be in the form a JSON, and the data can be rendered in a `Pandas` `DataFrame` by using the `pd.read_json()` method (more info [here](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_json.html)).

The entire `CZ_2010` dataset contains more than 50 weather stations and other features that is useful, depending on your use-case. More on the `CZ_2010` dataset, can be found [here](http://weather.whiteboxtechnologies.com/faq#Q13). For this example, I am only provided the weather data.


For this project, I purchased the three files used for this development from Whitebox Technologies. Obviously, there may be issues with licensing of these data, etc. however, the sole purpose of this project was to get stand-up a product as quickly as possible that can be elaborated to serve the entire community of users who are interested in these data.

This repo contains the scripts and notebooks that are used (or have) been used to stand up this API.





