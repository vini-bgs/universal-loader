from pathlib import Path
from loguru import logger
from src.config import FileConfig
from src.loader import FileLoader
from src.validator import SchemaValidator


FILES_DIR: Path = Path("files/")
SCHEMA: str = "dbo"

try:
    for file in FILES_DIR.iterdir():
        if file.suffix not in (".csv",):
            logger.warning(f"⚠️  Extensão '{file.suffix}' não suportada")
            continue

        config: FileConfig = FileConfig(
            file_path=str(file), schema_name=SCHEMA, table_name=file.stem
        )

        df = FileLoader(config).load()
        schema = SchemaValidator(config)._infer_dtypes(df)
        print(schema)

        logger.success("✅ Configuração concluída!")

except FileNotFoundError:
    logger.error(f"⚠️ Pasta '{FILES_DIR}/' não encontrada")
