import os

def list_parquet_files(directory):
    parquet_files = []
    for filename in os.listdir(directory):
        if filename.endswith(".parquet"):
            parquet_files.append(os.path.join(directory, filename))
    return parquet_files
