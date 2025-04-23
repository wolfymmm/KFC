import matplotlib.pyplot as plt
import pandas as pd
from ml_model import predict_wind


def get_filtered_data(df, selected_country, start_future, end_future):
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['date'] = df['last_updated'].dt.date

    df_country = df[df['country'].str.lower() == selected_country.lower()]
    df_country = df_country[(df_country['date'] >= start_future.date()) & (df_country['date'] <= end_future.date())]

    return df_country

def forecast_weather(df_country, df_model, model, start_future, end_future):
    forecast_data = {
        "date": [],
        "predicted_wind": [],
        "real_wind": [],
        "real_temp": [],
        "real_feelslike": [],
    }

    for d in pd.date_range(start_future, end_future):
        historical_data = df_country[df_country['date'] <= (d - pd.Timedelta(days=1)).date()]
        historical_data = historical_data.tail(3)

        if len(historical_data) > 0:
            X_new = historical_data[['temperature_celsius', 'humidity', 'cloud', 'uv_index']].mean()
        else:
            X_new = pd.Series([
                df_model['temperature_celsius'].mean(),
                df_model['humidity'].mean(),
                df_model['cloud'].mean(),
                df_model['uv_index'].mean()
            ], index=['temperature_celsius', 'humidity', 'cloud', 'uv_index'])

        prediction = predict_wind(model, X_new.to_frame().T)

        real = df_country[df_country['date'] == d.date()]

        # Отримуємо значення, або None, якщо відсутні
        real_wind = real['wind_kph'].values[0] if not real['wind_kph'].isna().all() else None
        real_temp = real['temperature_celsius'].values[0] if not real['temperature_celsius'].isna().all() else None
        real_feelslike = real['feels_like_celsius'].values[0] if 'feels_like_celsius' in real.columns and not real[
            'feels_like_celsius'].isna().all() else None

        forecast_data["date"].append(d.date())
        forecast_data["predicted_wind"].append(prediction)
        forecast_data["real_wind"].append(real_wind)
        forecast_data["real_temp"].append(real_temp)
        forecast_data["real_feelslike"].append(real_feelslike)

    return forecast_data


def plot_detailed_forecast(forecast_data):
    df_forecast = pd.DataFrame(forecast_data)
    df_forecast = df_forecast.dropna(subset=["real_wind", "real_temp", "real_feelslike"])

    fig, axs = plt.subplots(3, 1, figsize=(12, 15))

    axs[0].plot(df_forecast['date'], df_forecast['predicted_wind'], label='Прогноз', linestyle='--', color='blue')
    axs[0].plot(df_forecast['date'], df_forecast['real_wind'], label='Реальні дані', color='red')
    axs[0].set_title('Сила вітру (км/год)')
    axs[0].set_ylabel('Вітер')
    axs[0].legend()
    axs[0].grid(True)

    axs[1].plot(df_forecast['date'], df_forecast['real_wind'] / df_forecast['real_temp'], label='Реальне відношення',
                color='green')
    axs[1].plot(df_forecast['date'], df_forecast['predicted_wind'] / df_forecast['real_temp'],
                label='Прогнозоване відношення', color='orange', linestyle='--')
    axs[1].set_title('Відношення сили вітру до температури')
    axs[1].set_ylabel('Вітер / Температура')
    axs[1].legend()
    axs[1].grid(True)

    axs[2].plot(df_forecast['date'], df_forecast['real_wind'] / df_forecast['real_feelslike'],
                label='Реальне відношення', color='purple')
    axs[2].plot(df_forecast['date'], df_forecast['predicted_wind'] / df_forecast['real_feelslike'],
                label='Прогнозоване відношення', color='brown', linestyle='--')
    axs[2].set_title('Відношення сили вітру до температури по відчуттях')
    axs[2].set_ylabel('Вітер / Відчутна температура')
    axs[2].legend()
    axs[2].grid(True)

    for ax in axs:
        ax.set_xlabel("Дата")
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    plt.show()



def print_forecast_results(forecast_data):
    print("\n--- Прогноз сили вітру ---")
    for i in range(len(forecast_data["date"])):
        date = forecast_data["date"][i]
        predicted = round(forecast_data["predicted_wind"][i], 2)
        real = forecast_data["real_wind"][i]
        real_str = f"{round(real, 2)}" if real is not None else "немає даних"
        print(f"{date}: Прогноз = {predicted} км/год | {real_str} км/год")
