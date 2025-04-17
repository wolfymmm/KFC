import pandas as pd
import psycopg2

DB_HOST = "localhost"
DB_NAME = "weather"
DB_USER = "postgres"
DB_PASS = "momoa2005"

CSV_FILE = "GlobalWeather.csv"

def import_csv_to_postgres(csv_file, db_host, db_name, db_user, db_pass):
    try:
        conn = psycopg2.connect(host=db_host, database=db_name, user=db_user, password=db_pass)
        cur = conn.cursor()

        df = pd.read_csv(csv_file)
        df.rename(columns={
            'air_quality_PM2.5': 'air_quality_PM2_5',
            'air_quality_us-epa-index': 'air_quality_us_epa_index',
            'air_quality_gb-defra-index': 'air_quality_gb_defra_index'
        }, inplace=True)

        df = df.where(pd.notnull(df), None)

        for index, row in df.iterrows():
            try:
                sql = """
                    INSERT INTO weather_data (
                        country, location_name, latitude, longitude, timezone,
                        last_updated_epoch, last_updated, temperature_celsius, temperature_fahrenheit, condition_text,
                        wind_mph, wind_kph, wind_degree, wind_direction, pressure_mb,
                        pressure_in, precip_mm, precip_in, humidity, cloud,
                        feels_like_celsius, feels_like_fahrenheit, visibility_km, visibility_miles, uv_index,
                        gust_mph, gust_kph, air_quality_Carbon_Monoxide, air_quality_Ozone, air_quality_Nitrogen_dioxide,
                        air_quality_Sulphur_dioxide, air_quality_PM2_5, air_quality_PM10, air_quality_us_epa_index, air_quality_gb_defra_index,
                        sunrise, sunset, moonrise, moonset, moon_phase, moon_illumination
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """
                cur.execute(sql, (
                    row['country'], row['location_name'], row['latitude'], row['longitude'], row['timezone'],
                    row['last_updated_epoch'], row['last_updated'], row['temperature_celsius'], row['temperature_fahrenheit'], row['condition_text'],
                    row['wind_mph'], row['wind_kph'], row['wind_degree'], row['wind_direction'], row['pressure_mb'],
                    row['pressure_in'], row['precip_mm'], row['precip_in'], row['humidity'], row['cloud'],
                    row['feels_like_celsius'], row['feels_like_fahrenheit'], row['visibility_km'], row['visibility_miles'], row['uv_index'],
                    row['gust_mph'], row['gust_kph'], row['air_quality_Carbon_Monoxide'], row['air_quality_Ozone'], row['air_quality_Nitrogen_dioxide'],
                    row['air_quality_Sulphur_dioxide'], row['air_quality_PM2_5'], row['air_quality_PM10'], row['air_quality_us_epa_index'], row['air_quality_gb_defra_index'],
                    row['sunrise'], row['sunset'], row['moonrise'], row['moonset'], row['moon_phase'], row['moon_illumination']
                ))
            except psycopg2.Error as e:
                conn.rollback()
                print(f"Помилка при вставці рядка {index}: {e}")
                print(f"Дані рядка: {row.to_dict()}")
            except Exception as e:
                conn.rollback()
                print(f"Непередбачена помилка при обробці рядка {index}: {e}")
                print(f"Дані рядка: {row.to_dict()}")

        conn.commit()
        cur.close()
        conn.close()
        print("Імпорт завершено")

    except FileNotFoundError:
        print(f"Помилка: Файл '{csv_file}' не знайдено.")
    except psycopg2.Error as e:
        print(f"Помилка під час підключення до PostgreSQL: {e}")
    except Exception as e:
        print(f"Виникла непередбачена помилка: {e}")

if __name__ == "__main__":
    import_csv_to_postgres(CSV_FILE, DB_HOST, DB_NAME, DB_USER, DB_PASS)
