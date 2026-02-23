import pandas as pd
from sklearn.linear_model import LinearRegression
import datetime

def predict_inventory(filename='usage_log.csv'):
    df = pd.read_csv(filename)
    
    # Convert date to days since first day
    df['date'] = pd.to_datetime(df['date'])
    df['day_num'] = (df['date'] - df['date'].min()).dt.days

    predictions = {}
    for name in df['name'].unique():
        item_df = df[df['name'] == name]
        X = item_df[['day_num']]
        y = item_df['units_used']
        
        if len(X) < 2:
            predictions[name] = "Insufficient data"
            continue

        model = LinearRegression()
        model.fit(X, y)

        tomorrow = df['day_num'].max() + 1
        predicted_qty = model.predict([[tomorrow]])[0]
        predictions[name] = max(0, round(predicted_qty))

    return predictions
