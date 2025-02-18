import json
import pandas as pd
from clickhouse_driver import Client

def create_clickhouse_table(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    clickhouse_table_name = config['clickhouse_table']['name']
    clickhouse_engine = config['clickhouse_table']['engine']
    clickhouse_order_by = config['clickhouse_table']['order_by']
    clickhouse_fields = config['clickhouse_table']['fields']
    clickhouse_fields = {"dna_id": "Int32", **clickhouse_fields}
    client = Client('localhost')
    fields = ', '.join([f"{column} {data_type}" for column, data_type in clickhouse_fields.items()])
    query = f"""
    CREATE TABLE IF NOT EXISTS `{clickhouse_table_name}` (
        {fields}
    ) ENGINE = {clickhouse_engine}
    ORDER BY {clickhouse_order_by}
    """
    client.execute(query)
    print(f"ClickHouse table '{clickhouse_table_name}' created successfully.")

def insert_data_into_clickhouse(parquet_file_path, config_file):
    df = pd.read_parquet(parquet_file_path)
    df['dna_id'] = range(1, len(df) + 1)
    with open(config_file, 'r') as f:
        config = json.load(f)
    clickhouse_table_name = config['clickhouse_table']['name']
    clickhouse_fields = config['clickhouse_table']['fields']
    columns = ['dna_id'] + list(clickhouse_fields.keys())
    values = df[columns].values.tolist()
    client = Client('localhost')
    insert_query = f"INSERT INTO `{clickhouse_table_name}` ({', '.join(columns)}) VALUES"
    client.execute(insert_query, values)
    print(f"Data from Parquet file '{parquet_file_path}' inserted into '{clickhouse_table_name}'.")

def main(config_file, parquet_file_path):
    create_clickhouse_table(config_file)
    insert_data_into_clickhouse(parquet_file_path, config_file)
