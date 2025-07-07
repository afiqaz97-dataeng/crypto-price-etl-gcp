# Cloud Function: fetch_btc_price

## Purpose
Fetches the current Bitcoin price using the CoinGecko API, simulates 10,000 timestamped records, writes them to a Parquet file, and uploads to Google Cloud Storage.

## Deployment

To deploy manually:

```bash
gcloud functions deploy fetch_btc_price \
  --gen2 \
  --runtime python311 \
  --region asia-southeast1 \
  --source=. \
  --entry-point=fetch_btc_price \
  --trigger-http \
  --allow-unauthenticated \
  --project=crypto-etl-project-465203
