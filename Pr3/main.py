from datetime import datetime
from ml_model import train_model
from db import get_weather_data

from weather_prediction import (
    get_filtered_data,
    forecast_weather,
    plot_detailed_forecast,
    print_forecast_results
)

def main():
    selected_country = input("Введіть країну: ").strip()
    start_future = input("Дата початку прогнозу (YYYY-MM-DD): ").strip()
    end_future = input("Дата кінця прогнозу (YYYY-MM-DD): ").strip()

    start_future = datetime.strptime(start_future, "%Y-%m-%d")
    end_future = datetime.strptime(end_future, "%Y-%m-%d")
    df = get_weather_data()

    df_country = get_filtered_data(df, selected_country, start_future, end_future)

    # Тренування моделі та прогнозування
    df_model = df_country.dropna(subset=['temperature_celsius', 'humidity', 'cloud', 'uv_index', 'wind_kph'])
    model = train_model(df_model)
    forecast_data = forecast_weather(df_country, df_model, model, start_future, end_future)

    print_forecast_results(forecast_data)
    plot_detailed_forecast(forecast_data)

if __name__ == "__main__":
    main()
