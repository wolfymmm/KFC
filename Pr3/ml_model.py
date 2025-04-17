from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def train_model(df_model):
    X = df_model[['temperature_celsius', 'humidity', 'cloud', 'uv_index']]
    y = df_model['wind_kph']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict_wind(model, X_new):
    return model.predict(X_new)[0]
