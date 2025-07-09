import requests
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from google.cloud import storage
import os
from io import BytesIO
import numpy as np

def fetch_btc_price(request=None):
    try:
        # Use CoinGecko's simple price endpoint (more reliable)
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd"
        }
        headers = {
            "Accept": "application/json",
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        price = response.json()["bitcoin"]["usd"]

        # Simulate 10,000 records by generating timestamps
        now = datetime.datetime.now(datetime.timezone.utc)
        timestamps = [now - datetime.timedelta(seconds=60 * i) for i in range(10000)]
        # Simulate realistic fluctuation around the fetched price
        np.random.seed(42)
        price_fluctuations = np.random.normal(loc=0, scale=30, size=10000)  # ±$30 variance
        simulated_prices = np.round(price + price_fluctuations, 2)

        df = pd.DataFrame({
        "timestamp": timestamps,
        "price_usd": [float(price)] * 10000  # <-- force float
        })

        df["price_usd"] = df["price_usd"].astype(float)


        print(f"✅ Simulated {len(df)} BTC records")

        # Convert to Parquet using pyarrow
        table = pa.Table.from_pandas(df)
        parquet_buffer = BytesIO()
        pq.write_table(table, parquet_buffer)

        # Upload to GCS
        today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%d_%H%M%S')
        bucket_name = "crypto-etl-bucket-af"  # replace if needed
        filename = f"staging/btc_price_{today}.parquet"

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(parquet_buffer.getvalue(), content_type="application/octet-stream")

        print(f" Uploaded {filename} to GCS")
        return f"Uploaded {len(df)} records to {filename}", 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return f"Error: {e}", 500
    
# # To test script in local 
# if __name__ == "__main__":
#     class DummyRequest:
#         def __init__(self):
#             self.args = {}

#     print(fetch_btc_price(DummyRequest()))
