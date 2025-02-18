import os
import sys
import json
import logging
from my_package.config import load_config
from my_package.inspectdb import generate_api_endpoints, validate_paths
from my_package.parquet import generate_config_from_parquet
from my_package.clickhouse import main as clickhouse_main
from my_package.utils import list_parquet_files

def main():
    try:
        config = load_config()
        required_keys = ["base_dir", "project_name", "app_name", "database_alias"]
        for key in required_keys:
            if key not in config:
                raise KeyError(f"Missing required configuration key: '{key}'")

        base_dir = config["base_dir"]
        project_dir = config["project_name"]
        app_dir = config["app_name"]
        database_alias = config["database_alias"]

        project_path = os.path.join(base_dir, project_dir)
        app_path = os.path.join(project_path, app_dir)

        validate_paths(project_path, app_path)

        parquet_directory = config.get("parquet_path", "./")
        config_directory = config.get("config_path", "./")
        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

        parquet_files = list_parquet_files(parquet_directory)
        for parquet_file in parquet_files:
            file_name = os.path.basename(parquet_file)
            output_config_file = os.path.join(config_directory, f"{os.path.splitext(file_name)[0]}_config.json")
            print(f"Generating config for: {file_name}")
            generate_config_from_parquet(file_name, output_config_file)
            print(f"Running write_clickhouse_table_2 for: {file_name}")
            clickhouse_main(output_config_file, parquet_file)

        print("Running append_endpoints_using_inspectdb_1.py at the end of the process.")
        generate_api_endpoints(project_path, app_path, database_alias)

    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
