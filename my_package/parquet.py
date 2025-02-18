import os
import sys
import pandas as pd
import json

def load_config():
    config_path = os.path.join(os.getcwd(), "config.json")
    try:
        with open(config_path, "r") as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found: {config_path}")
        sys.exit(1)

def generate_config_from_parquet(file_name, output_file_name):
    config = load_config()
    parquet_dir = config.get("parquet_path", "./")
    config_dir = config.get("config_path", "./")
    parquet_file_path = os.path.join(parquet_dir, file_name)
    output_file_path = os.path.join(config_dir, output_file_name)
    endpoint = os.path.splitext(os.path.basename(file_name))[0]
    clickhouse_table_name = endpoint.lower()
    df = pd.read_parquet(parquet_file_path)
    model_fields = {}
    clickhouse_fields = {}
    for column, dtype in df.dtypes.items():
        model_field = map_dtype_to_django_field(column, dtype)
        clickhouse_field = map_dtype_to_clickhouse_field(column, dtype)
        model_fields[column] = model_field
        clickhouse_fields[column] = clickhouse_field
    config_data = {
        "app_name": "myapp",
        "model_name": "ComplicatedModel",
        "model_fields": model_fields,
        "serializer_name": "ComplicatedModelSerializer",
        "view_name": "ComplicatedModelViewSet",
        "url_path": endpoint,
        "clickhouse_table": {
            "name": clickhouse_table_name,
            "engine": "MergeTree",
            "order_by": "id",
            "fields": clickhouse_fields
        }
    }
    os.makedirs(config_dir, exist_ok=True)
    with open(output_file_path, 'w') as config_file:
        json.dump(config_data, config_file, indent=4)
    print(f"Configuration file generated at: {output_file_path}")

def map_dtype_to_django_field(column, dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return f"models.IntegerField()"
    elif pd.api.types.is_float_dtype(dtype):
        return f"models.FloatField()"
    elif pd.api.types.is_bool_dtype(dtype):
        return f"models.BooleanField()"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return f"models.DateTimeField()"
    elif pd.api.types.is_string_dtype(dtype):
        return f"models.CharField(max_length=255)"
    else:
        return f"models.TextField()"

def map_dtype_to_clickhouse_field(column, dtype):
    if pd.api.types.is_integer_dtype(dtype):
        return "UInt32"
    elif pd.api.types.is_float_dtype(dtype):
        return "Float32"
    elif pd.api.types.is_bool_dtype(dtype):
        return "UInt8"
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return "DateTime"
    elif pd.api.types.is_string_dtype(dtype):
        return "String"
    else:
        return "String"
