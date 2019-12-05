# pandas-api

![](./docs/giant-panda-in-the-forest-banner.png)

Pandas is an awesome data manipulation and analysis library written for Python. It is an
open source project that provides high-performance, easy-to-use data structures and data analysis tools.

The goal of the samples in this repository is to demonstrate the use of Pandas' `apply` method to dynamically enrich a Dataframe using data from APIs. The reality of manipulating data is that your results will only be as good as your input (**Garbage in, Garbage out**). Because APIs allows us to programmatically share and retrieve data between systems, leveraging Pandas get input directly from APIs allow us to gather better quality data at using a more scalable approach.

## requirements

In order to execute the examples included in this repository, you will need the following libraries:

* Python 3.6+

* pandas

* requests

We'll also use the geocoding APIs from [Google GCP](https://console.cloud.google.com/) and [OpenCage Data](https://opencagedata.com/). Both of these services allow
us to use geocoding data to convert addresses (like a street address) into geographic coordinates, and vice versa. Note that you will have to sign up to these services in order to obtain an API key for the requests.

## Sample Data

The example scripts in this repo will use the sample tabular data shown below. It represents a list of sites with addresses. In some cases, only partial address information is available. Some locations are missing street address, postal codes, or are not properly formatted.

| location_name    | address                                           |
| ---------------- | ------------------------------------------------- |
| Corporate HQ     | 1800 W Balboa Boulevard Newport Beach  California |
| Marketing        | 10 Hudson Yards  New York NY                      |
| London Office    | 25 Canada Square Canary Wharf  London             |
| Patch Branch     | 7406 Oak Ave. Patchogue, NY 11772                 |
| Goldsboro        | 59 North Dr. Goldsboro, NC 27530                  |
| Davenport Branch | 52804                                             |


## Sample Output

Using the `pandas_api_demo.py` in this repository, we demonstrate an easy method enrich our current data with additional information. In some cases, we are even able to normalize our data using information gathered through the APIs. Below is a sample output data from the script.

| location_name    | address                                           | latitude   | longitude    | formatted_address                                                 | accuracy         |
| ---------------- | ------------------------------------------------- | ---------- | ------------ | ----------------------------------------------------------------- | ---------------- |
| Corporate HQ     | 1800 W Balboa Boulevard Newport Beach  California | 33.6079545 | -117.9250816 | 1800 W Balboa Blvd, Newport Beach, CA 92663, USA                  | ROOFTOP          |
| Marketing        | 10 Hudson Yards  New York NY                      | 40.7527246 | -74.0016428  | 10 Hudson Yards 24th Floor, 347 10th Ave, New York, NY 10001, USA | ROOFTOP          |
| London Office    | 25 Canada Square Canary Wharf  London             | 51.5040016 | -0.0177746   | Citigroup Centre, Canary Wharf, London E14, UK                    | ROOFTOP          |
| Patch Branch     | 7406 Oak Ave. Patchogue, NY 11772                 | 40.7689237 | -73.00955    | Oak St, Patchogue, NY 11772, USA                                  | GEOMETRIC_CENTER |
| Goldsboro        | 59 North Dr. Goldsboro, NC 27530                  | 35.3913609 | -77.963208   | North Dr, Goldsboro, NC 27534, USA                                | GEOMETRIC_CENTER |
| Davenport Branch | 52804                                             | 41.5292258 | -90.6867939  | Davenport, IA 52804, USA                                          | APPROXIMATE      |
