# pandas-api

<div align="center">
<img src="./docs/giant-panda-in-the-forest-banner.png">

</div>

Pandas is an awesome data manipulation and analysis library written for Python. It is an
open source project that provides high-performance, easy-to-use data structures and data analysis tools.

The goal of the samples in this repository is to demonstrate the use of Pandas' `apply` method to dynamically enrich a Dataframe using data from APIs. The reality of manipulating data is that your results will only be as good as your input (**Garbage in, Garbage out**). Because APIs allows us to programmatically share and retrieve data between systems, leveraging Pandas get input directly from APIs allow us to gather better quality data at using a more scalable approach.

## requirements

In order to execute the examples included in this repository, you will need the following libraries:

* Python 3.6+

* pandas

* requests

We'll also use the geocoding API from [Google GCP](https://console.cloud.google.com/) . The API service allow us to use geocoding data to convert addresses (like a street address) into geographic coordinates, and vice versa. Note that you will have to [sign up](https://cloud.google.com/maps-platform/) in order to obtain an API key for the requests. [Google offers a credit](https://cloud.google.com/maps-platform/user-guide/account-changes/#no-plan) that allows these APIs call to be made for free, in most cases.

## Sample Data

The example scripts in this repo will use Pandas to load data from CSV. The simple data set contains a list of sites with addresses. In some cases, only partial address information is available. Some locations are missing street address, postal codes, or are not properly formatted.

| location_name    | address                                           |
| ---------------- | ------------------------------------------------- |
| Corporate HQ     | 1800 W Balboa Boulevard Newport Beach  California |
| Marketing        | 10 Hudson Yards  New York NY                      |
| London Office    | 25 Canada Square Canary Wharf  London             |
| Patch Branch     | 7406 Oak Ave. Patchogue, NY 11772                 |
| Goldsboro        | 59 North Dr. Goldsboro, NC 27530                  |
| Davenport Branch | 52804                                             |


## Sample Output

Using the `pandas_api_demo.py` in this repository, we'll demonstrate an easy method enrich our current data with additional information. In some cases, you'll see that we are even able to normalize our data using information gathered through the APIs. Below is a sample output data from the script. Notice how original address field compares with the 'formatted_address` field as it was returned from Google's API.

| location_name    | address                                           | latitude   | longitude    | formatted_address                                                 | accuracy         |
| ---------------- | ------------------------------------------------- | ---------- | ------------ | ----------------------------------------------------------------- | ---------------- |
| Corporate HQ     | 1800 W Balboa Boulevard Newport Beach  California | 33.6079545 | -117.9250816 | 1800 W Balboa Blvd, Newport Beach, CA 92663, USA                  | ROOFTOP          |
| Marketing        | 10 Hudson Yards  New York NY                      | 40.7527246 | -74.0016428  | 10 Hudson Yards 24th Floor, 347 10th Ave, New York, NY 10001, USA | ROOFTOP          |
| London Office    | 25 Canada Square Canary Wharf  London             | 51.5040016 | -0.0177746   | Citigroup Centre, Canary Wharf, London E14, UK                    | ROOFTOP          |
| Patch Branch     | 7406 Oak Ave. Patchogue, NY 11772                 | 40.7689237 | -73.00955    | Oak St, Patchogue, NY 11772, USA                                  | GEOMETRIC_CENTER |
| Goldsboro        | 59 North Dr. Goldsboro, NC 27530                  | 35.3913609 | -77.963208   | North Dr, Goldsboro, NC 27534, USA                                | GEOMETRIC_CENTER |
| Davenport Branch | 52804                                             | 41.5292258 | -90.6867939  | Davenport, IA 52804, USA                                          | APPROXIMATE      |


## Getting Started With the Script

First, you need to clone or fork this repository to ensure that you have access to all of the files.

```sh
git clone https://github.com/ttafsir/pandas-api-demo.git
```

The next step before we can run our script is to ensure that we have all of the requirements installed. We can do so using `pip` and the `requirements.txt` file in this repo.

```sh
pip install -r requirements.txt
```

### Using the demo script

As shown in the snippet below, the `pandas_api_demo.py` file loads the Google API key from a `.env` file.

```python
import datetime
import os
import pandas as pd
import requests


# load API key from the .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GCP_API_KEY")
except ImportError:
    GOOGLE_API_KEY = ''

```

I have excluded the `.env` file from version control, so you would have to create a file and save it as `.env` with your API key. Below is an example showing the contents of a `.env` file.

```ini
# .env file example
GCP_API_KEY=AIzSKjdl_NlhCETCWg23kjkP0nS6nw376zM

```

### Running the script

execute `python pandas_api_demo.py` in a terminal window as shown below. If API call was successful, you should see the columns: `latitude, longitude, formatted_address, accuracy`. The output will also be save to a file called `output_locations.csv`.

```sh
$ python pandas_api_demo.py
      location_name                                            address   latitude   longitude                                  formatted_address          accuracy
0      Corporate HQ  1800 W Balboa Boulevard Newport Beach  California  33.607954 -117.925082   1800 W Balboa Blvd, Newport Beach, CA 92663, USA           ROOFTOP
1         Marketing                       10 Hudson Yards  New York NY  40.752725  -74.001643  10 Hudson Yards 24th Floor, 347 10th Ave, New ...           ROOFTOP
2     London Office              25 Canada Square Canary Wharf  London  51.504002   -0.017775     Citigroup Centre, Canary Wharf, London E14, UK           ROOFTOP
3      Patch Branch                  7406 Oak Ave. Patchogue, NY 11772  40.768924  -73.009550                   Oak St, Patchogue, NY 11772, USA  GEOMETRIC_CENTER
4         Goldsboro                   59 North Dr. Goldsboro, NC 27530  35.391361  -77.963208                 North Dr, Goldsboro, NC 27534, USA  GEOMETRIC_CENTER
5  Davenport Branch                                              52804  41.529226  -90.686794                           Davenport, IA 52804, USA       APPROXIMATE

```

### Understanding the script

Below is the entire code for the demo. We'll go over the relevant sections for this demo.

```python
import datetime
import os
import pandas as pd
import requests


# load API key from the .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
    GOOGLE_API_KEY = os.getenv("GCP_API_KEY")
except ImportError:
    GOOGLE_API_KEY = ''

# Alternatively, you can set your API key manually
# GCP_API_KEY = 'AIzSKjdl_NlhCETCWg23kjkP0nS6nw376zM'

# Basic settings
input_filename  = 'input_locations.csv'
output_filename = 'output_locations.csv'
GEOCODE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


# We Define a function to call the google geocoding API
# The parameter 'address' refers to each row of the 'address' column in our
# input data. This will be passed as input to the API.
# We're using the Requests library to make an HTTP GET request to the url
# and we receive the response using the ‘.json’ method.
def retrieve_map_data(url, address=None, api_key=None):
    """
    Returns the results from Google Maps Geocoding API.

    @param address: String address or postal code. For Example ""
    @param api_key: String API key for GCP.
                    If supplied, requests will use your allowance from the Google API. If not, you
                    will be limited to the free usage of 2500 requests per day.

    """
    if GOOGLE_API_KEY:
        api_key = GOOGLE_API_KEY

    endpoint = f"{url}?address={address}&key={api_key}"
    r = requests.get(endpoint)

    if r.status_code not in range(200, 299):
        return (False, None)
    try:
        results = r.json()['results'][0]
        return (True, results)
    except Exception as e:
        return (False, str(e))


# Now we define a function that will be used with Pandas` .apply method
# to enrich our data. The 'row' argument is used by the .apply method to
# pass each row through the function. We supply additional keyword arguments
# **kwargs. These arguments include kwargs.get('column') and kwargs.get('url')
# to pass the url for the API and the column name that contains our address data
def enrich_data(row, **kwargs):
    """
    Dynamically Augment API results to pd Dataframe

    @param url: url for the GCP geocode service
    @param column: column in the Dataframe that maps to address data

    """
    # This is the column contain our address or zip code data
    column_name = kwargs.get('column')
    if column_name is not None:
        address = row[column_name]

        # Fetch API results
        url = kwargs.get('url')
        succeeded, results = retrieve_map_data(url, address=address)

        # Update Dataframe
        if succeeded:
            row['latitude'] = results['geometry']['location']['lat']
            row['longitude'] = results['geometry']['location']['lng']
            row['formatted_address'] = results['formatted_address']
            row['accuracy'] = results['geometry']['location_type']
    return row


def main():

    # Load the CSV to a Pandas Dataframe
    df = pd.read_csv(input_filename, encoding='utf8')

    # Enrich Data dynamically using pandas' apply method to apply the 'enrich_data` function
    # to the rows of the dataframe
    rest_api_df = df.apply(enrich_data, axis=1, url=GEOCODE_API_URL, column='address')

    print(rest_api_df)

    # Save Output Data
    rest_api_df.to_csv(output_filename, encoding='utf8', index=False)


if __name__ == '__main__':
    main()
```