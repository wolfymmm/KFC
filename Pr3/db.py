import pandas as pd
from sqlalchemy import create_engine

DB_HOST = "localhost"
DB_NAME = "weather"
DB_USER = "postgres"
DB_PASS = "momoa2005"


def get_weather_data():
    engine = create_engine(f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}')
    query = """
    SELECT country, location_name, last_updated, wind_kph, temperature_celsius, feels_like_celsius, humidity, cloud, uv_index
    FROM weather_data
    WHERE wind_kph IS NOT NULL AND last_updated IS NOT NULL
    """
    df = pd.read_sql(query, engine)
    return df
