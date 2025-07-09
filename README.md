
# 🚀 Crypto Price ETL Pipeline on GCP

A data engineering project that extracts Bitcoin price data from the CoinGecko API, stores it in Google Cloud Storage as Parquet files, and transforms it using Dataform into curated BigQuery tables.

---

## 📦 Project Structure

```
crypto-price-etl-gcp/
│
├── cloud_function/                # Cloud Function code for ETL (Python)
│   ├── main.py                    # Entry-point script to fetch and upload BTC data
│   └── requirements.txt           # Dependencies for cloud function
│
├── definitions/                    # Dataform repo for transformation              
│   └── curated_btc_prices.sqlx     # Compilable SQLX models
│
├── deploy/                        # Deployment YAMLs/scripts for cloud function and cloud builds
│   └── deploy.yaml                # (Optional) For automated builds
│
└── sql/                           # SQL files for manual execution
|    ├── 01_create_dataset.sql     # Creates the BigQuery dataset
|    └── 02_create_external_table.sql # Creates external table from Parquet in GCS
|
└── .gitignore                    # ignore cache when pushing to the git
└──  README.md                    # Documentation of Projects
└── workflow_settings.yaml        # Configuration and packages file for dataform transformation

```

---

## 🛠️ Tech Stack

| Component          | Tool / Service               |
|-------------------|------------------------------|
| Language           | Python 3.11                  |
| Data Source        | CoinGecko API                |
| Storage            | Google Cloud Storage (GCS)   |
| Transformation     | Dataform (SQLX on BigQuery)  |
| Orchestration      | Cloud Functions (Serverless) |
| Format             | Parquet                      |
| Destination        | BigQuery                     |

---

## 🧪 Pipeline Flow

1. **Extract**  
   - BTC prices are fetched for the past 7 days at 1-minute intervals using the CoinGecko API.
   - Disclaimer: To simulate sufficient data volume for Parquet file justification, I generated or extended records to reach ~10,000 rows due to API limitations and stability.
2. **Load**  
   - Data is converted to Parquet format with `pyarrow` and uploaded to a GCS bucket.
3. **Stage**  
   - An external BigQuery table is created over the Parquet data in `crypto_etl_staging`.
4. **Transform**  
   - Using Dataform, the staging table is transformed and written to a curated dataset.

---

## 🔧 How to Deploy

### 1. Deploy the Cloud Function

```bash
gcloud functions deploy fetch_btc_price   --runtime python311   --region asia-southeast1   --source ./cloud_function   --entry-point fetch_btc_price   --trigger-http   --allow-unauthenticated
```

> The function will save the Parquet file to `gs://crypto-etl-bucket-af/staging/`

---

### 2. Create BigQuery Dataset & External Table

```bash
bq query --use_legacy_sql=false < sql/01_create_dataset.sql
bq query --use_legacy_sql=false < sql/02_create_external_table.sql
```

---

### 3. Setup Dataform

- Link your GitHub repo in [Dataform UI](https://console.cloud.google.com/dataform)
- Create a workspace (e.g. `dev-afiq`)
- Move your `.sqlx` models into `dataform/definitions/`
- Compile & Run the transformations

---

## 🧠 Example SQLX Model (curated_btc_prices.sqlx)

```sqlx
config {
  type: "table",
  schema: "dataform"
}

select
  timestamp,
  price_usd
from
  `${gcp_project_id}.crypto_etl_staging.btc_price_external`
```

---

## 🔐 GitHub + Dataform Integration

- Created [Fine-Grained Personal Access Token]
- Granted `Contents: Read & Write` on selected repo
- Stored securely in **GCP Secret Manager**
- Linked in Dataform for remote Git repo sync

---

## 📈 Sample Output

Once deployed, you’ll have:

| Table                       | Type           | Description                         |
|----------------------------|----------------|-------------------------------------|
| `btc_price_external`       | External Table | Raw Parquet data from GCS           |
| `curated_btc_prices`       | Table (SQLX)   | Transformed table using Dataform    |



---

## 👨‍💻 Author

**Afiq Azizi**  
Data Engineer | Project: `crypto-price-etl-gcp`

---

## 📄 License

MIT License
