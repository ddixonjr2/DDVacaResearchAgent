import os
import pandas as pd

from wwo_hist import retrieve_hist_data
from agents import function_tool
from dotenv import load_dotenv
from urllib.parse import quote
from datetime import datetime, timedelta
from vaca_user_context import *

def get_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get('WWO_API_KEY')
    if api_key is None or api_key == '':
        raise ValueError('No WWO_API_KEY found')
    else:
        return api_key

def get_historic_weather_data(location: str) -> list[pd.DataFrame]:
    '''
    Retrieves historic weather data for a location 
    
    Args:
    - location: A string representing the location (city, country, postal code)
    '''
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    try:
        api_key = get_api_key()
        print(f'Calling 3rd party lib to retrieve weather data for {location}...')
        repsonse_df = retrieve_hist_data(
            api_key=api_key,
            location_list=[location], 
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            frequency='daily',
            export_csv=True,
            store_df=True,
            response_cache_path=os.path.join(os.getcwd(), 'hist_weather_cache')
        )
        return repsonse_df[0]
    except Exception as e:
        print(f'Failed to retrieve historical weather data:\n{e}')
        return None

@function_tool
def get_historical_weather_description(location: str) -> str:
    return get_historical_weather_desc(location)
    
def get_historical_weather_desc(location: str) -> str:
    '''
    Retrieves historic weather, calculates averages, and returns a description summarizing the averages.
    
    Args:
    - location: A string representing the location (city, country, postal code)
    '''
    print(f'Invoking get_historical_weather_description(location: {location})...')
    encoded_location = quote(location)
    print(f'encoded_location: {encoded_location})...')

    try: 
        hist_data_df = get_historic_weather_data(encoded_location)
        if hist_data_df is not None and not hist_data_df.empty:
            avg_temp = pd.to_numeric(hist_data_df['tempC']).mean()
            avg_humidity = pd.to_numeric(hist_data_df['humidity']).mean()
            avg_cloudcover = pd.to_numeric(hist_data_df['cloudcover']).mean()
            description = f'''
                Average temperature for the last 30 days in {location} was {avg_temp:.2f}°C
                with an average humidity of {avg_humidity:.2f}% and average cloud cover of {avg_cloudcover:.2f}%.
            '''
            print(f'...get_historical_weather_description(location: {location}) returning:\n{description}')
            return description
        else:
            return f'No historical weather data available for {location}.'
    except Exception as e:
        print(f'Failed to get historical weather description for {location}:\n{e}')
        return f'Error retrieving weather data for {location}.'

def test():
    try:
        response = get_historical_weather_desc('Florianopolis, Brazil')
        print(f'The test response is:\n{response}')
    except Exception as e:
        print(f'Test failed:\n{e}')

if __name__ == '__main__':
    test()
