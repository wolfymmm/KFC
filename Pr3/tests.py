import unittest
from datetime import datetime

from db import get_weather_data
from ml_model import train_model
from weather_prediction import get_filtered_data, forecast_weather


class TestWeatherForecasting(unittest.TestCase):

    def test_get_weather_data(self):
        df = get_weather_data()
        self.assertFalse(df.empty, "Дані про погоду не повинні бути порожніми.")

    def test_train_model(self):
        df = get_weather_data()
        df_model = df.dropna(subset=['temperature_celsius', 'humidity', 'cloud', 'uv_index', 'wind_kph'])

        if df_model.empty:
            self.skipTest("Недостатньо даних для тренування моделі.")
        else:
            model = train_model(df_model)
            self.assertIsNotNone(model, "Модель повинна бути успішно натренована.")

    def test_forecast_weather(self):
        df = get_weather_data()
        selected_country = "Ukraine"
        start_future = datetime(2025, 4, 10)
        end_future = datetime(2025, 4, 14)

        df_country = get_filtered_data(df, selected_country, start_future, end_future)
        df_model = df.dropna(subset=['temperature_celsius', 'humidity', 'cloud', 'uv_index', 'wind_kph'])

        if df_model.empty or df_country.empty:
            self.skipTest("Недостатньо даних для прогнозу.")
        else:
            model = train_model(df_model)
            forecast_data = forecast_weather(df_country, df_model, model, start_future, end_future)
            self.assertTrue(len(forecast_data['date']) > 0, "Дані прогнозу не повинні бути порожніми.")

    def test_health_check(self):
        try:
            df = get_weather_data()
            self.assertFalse(df.empty, "База даних нічого не повернула.")

            df_model = df.dropna(subset=['temperature_celsius', 'humidity', 'cloud', 'uv_index', 'wind_kph'])
            self.assertFalse(df_model.empty, "Недостатньо даних для тренування моделі.")

            model = train_model(df_model)

            selected_country = "Ukraine"
            start_future = datetime(2025, 4, 15)
            end_future = datetime(2025, 4, 20)
            df_country = get_filtered_data(df, selected_country, start_future, end_future)

            forecast_data = forecast_weather(df_country, df_model, model, start_future, end_future)
            self.assertTrue(len(forecast_data['date']) > 0, "Не вдалося зробити прогноз.")
        except Exception as e:
            self.fail(f"Health check не пройдено: {str(e)}")


if __name__ == '__main__':
    unittest.main()
