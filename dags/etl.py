from airflow import DAG
from datetime import datetime, timedelta
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from airflow.utils.dates import days_ago
import json

# Define the DAG
with DAG(
    dag_id='nasa_postgres',
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags=['nasa', 'postgres'],
    catchup=False
) as dag:

    ## Step 1: Create a table if it does not exist
    @task()
    def create_table():
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        create_table_query = """
            CREATE TABLE IF NOT EXISTS apod_data(
                date DATE PRIMARY KEY,
                title VARCHAR(100),
                explanation TEXT,
                url VARCHAR(100),
                media_type VARCHAR(50)
            )
        """
        postgres_hook.run(create_table_query)

    ## Step 2: Fetch data from the NASA APOD API
    extract_apod = SimpleHttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',  # Connection ID defined in Airflow for the NASA API   
        endpoint='planetary/apod?api_key={{ conn.nasa_api.extra_dejson.api_key }}',
        method='GET',
        response_filter=lambda response: response.json(),
        log_response=True
    )

    ## Step 3: Transform the data
    @task()
    def transform_apod(data):
        apod_data = {
            "title": data.get('title', ''),
            "explanation": data.get('explanation', ''),
            "url": data.get('url', ''),
            "date": data.get('date', ''),
            "media_type": data.get('media_type', '')
        }
        return apod_data

    ## Step 4: Insert the data into the Postgres table
    @task()
    def load_apod_to_postgres(apod_data):
        postgres_hook = PostgresHook(postgres_conn_id='my_postgres_connection')
        insert_query = """
            INSERT INTO apod_data (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (date) DO NOTHING
        """
        postgres_hook.run(insert_query, parameters=[
            apod_data['title'],
            apod_data['explanation'],
            apod_data['url'],
            apod_data['date'],
            apod_data['media_type']
        ])

    # Define task dependencies
    create_table_task = create_table()  # Task for creating the table
    transformed_data = transform_apod(extract_apod.output)  # Transform task uses output from extract_apod
    create_table_task >> extract_apod >> transformed_data >> load_apod_to_postgres(transformed_data)

