#! /usr/bin/python

"""
Python script to demonstrate the use of the Pandas library to augment API data.

The script loads a list of addresses from csv input data. Then, it uses
the Google geocoding API to augment the existing data. An output file of the results is
generated after the update.

This example demonstrates a basic use the pandas apply method to enrich a dataframe with API data.

Tafsir Thiam
@ttafsir
"""
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


# Settings
input_filename  = 'input_locations.csv'
output_filename = 'output_locations.csv'
GEOCODE_API_URL = "https://maps.googleapis.com/maps/api/geocode/json"


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

    # Enrich Data dynamically using pandas' apply method
    rest_api_df = df.apply(enrich_data, axis=1, url=GEOCODE_API_URL, column='address')

    print(rest_api_df)

    # Save Output Data
    rest_api_df.to_csv(output_filename, encoding='utf8', index=False)


if __name__ == '__main__':
    main()