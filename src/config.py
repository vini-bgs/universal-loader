from dataclasses import dataclass


@dataclass
class FileConfig:
    file_path: str
    schema_name: str
    table_name: str
    delimiter: str = ";"
    encoding: str = "utf-8"
    if_exist: str = "replace"
    normalize_columns: bool = True
