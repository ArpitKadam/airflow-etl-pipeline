# Airflow ETL Pipeline

This repository contains an ETL (Extract, Transform, Load) pipeline built using Apache Airflow. The pipeline is designed to automate the process of extracting data, transforming it, and loading it into a target data store.

## Technologies Used

- **Apache Airflow**: Orchestrates the ETL processes.
- **Python**: Programming language used for writing DAGs and transformations.
- **Docker**: Containerization platform for bundling the application stack.
- **PostgreSQL (or other databases)**: Used as the target data store.
- **Astronomer**: (Optional) Platform for running Airflow.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ArpitKadam/airflow-etl-pipeline.git
   ```

2. **Install dependencies:**
   ```bash
   cd airflow-etl-pipeline
   pip install -r requirements.txt
   ```

3. **Docker Setup (optional):**
   ```bash
   docker-compose up -d
   ```

4. **Database Setup:**
   - Ensure PostgreSQL (or other) database is running.

## Usage

1. **Run the Airflow web server:**
   ```bash
   airflow webserver -p 8080
   ```

2. **Run the Airflow scheduler:**
   ```bash
   airflow scheduler
   ```

## Pipeline Workflow

- **Extract**: Data is fetched from a specified source.
- **Transform**: Data is cleaned, processed, and transformed.
- **Load**: Transformed data is loaded into a target data store.

## Directory Structure

```
airflow-etl-pipeline/
├── dags/                     # Airflow DAGs
│   └── etl.py                # Main ETL pipeline DAG file
├── plugins/                  # Custom Airflow operators or hooks
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker Compose configuration
├── requirements.txt          # Python dependencies
└── airflow_settings.yaml     # Airflow-specific settings
```

## License

This project is licensed under the MIT License.
