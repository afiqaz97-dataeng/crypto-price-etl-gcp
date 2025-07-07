-- Create external table in BigQuery from GCS Parquet files

CREATE OR REPLACE EXTERNAL TABLE `crypto-etl-project-465203.staging_crypto.ext_btc_price_parquet`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://crypto-etl-bucket-af/staging/*.parquet']
);
