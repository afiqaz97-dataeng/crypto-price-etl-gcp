#!/bin/bash

# Create BigQuery dataset in the correct location
bq mk \
  --location=asia-southeast1 \
  --dataset crypto-etl-project-465203:staging_crypto