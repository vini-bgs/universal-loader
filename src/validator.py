import pandas as pd
from loguru import logger
from src.config import FileConfig


class SchemaValidator:
    def __init__(self, config: FileConfig):
        self.config = config

    def _infer_dtypes(self, df: pd.DataFrame) -> dict:
        """Infere qual o tipo de cada coluna da tabela."""
        try:
            logger.info("🏁  Iniciando a inferência de tipagem...")
            schema: dict = dict()
            sample_df: pd.DataFrame = df.head(1000)

            for col in df.columns:
                sample = sample_df[col].dropna()

                if len(sample) == 0:
                    schema[col] = "str"
                    continue

                converted = pd.to_numeric(sample, errors="coerce")
                if converted.notna().mean() > 0.8:
                    if converted.dropna().astype(str).str.len().mean() >= 6:
                        schema[col] = "str"
                        continue
                    if (converted.dropna() % 1 == 0).all():
                        schema[col] = "int"
                        continue
                    else:
                        schema[col] = "float"
                        continue

                converted = pd.to_datetime(sample, errors="coerce", format="mixed")
                if converted.notna().mean() > 0.8:
                    schema[col] = "date"
                    continue

                schema[col] = "str"

            logger.success("✅  Schema concluído!")

            return schema

        except ValueError as err:
            logger.error(f"⛔ Erro no formato de dados: {err}")
        except KeyError as err:
            logger.error(f"⛔ Coluna não encontrada: {err}")
        except Exception as err:
            logger.error(f"⛔ Erro inesperado: {err}")
