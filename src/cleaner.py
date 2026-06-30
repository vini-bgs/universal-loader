from loguru import logger
from src.config import FileConfig
import pandas as pd
import re


class DataCleaner:
    def __init__(self, config: FileConfig):
        self.config = config

    def _normalize_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normaliza as colunas para snake_case sem acentos."""

        try:
            df.columns = (
                df.columns.str.strip()
                .str.lower()
                .str.replace(" ", "_", regex=False)
                .str.normalize("NFKC")
                .str.encode("ascii", errors="ignore")
                .str.decode("utf-8")
            )
            logger.info("📝  Colunas normalizadas para snake_case")

        except Exception as err:
            logger.error(f"⛔  {err}")

        return df

    def _strip_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Filtra as colunas do tipo string do DataFrame e aplica o .strip() nelas."""

        try:
            str_col = df.select_dtypes(include="object").columns
            df[str_col] = df[str_col].apply(lambda col: col.str.strip())

        except Exception as err:
            logger.error(f"⛔  {err}")
        return df

    def _clean_id_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Trata as colunas de ID que possuem letra antes do ID
        por exemplo: t23123716283761782631

        O código retira o 't' deixando apenas o ID
        """
        pattern = re.compile(r"^[a-zA-Z]+\d{18}$")

        for col in df.select_dtypes(include="object").columns:
            sample = df[col].dropna().astype(str).head(20)

            if sample.str.match(pattern).mean() > 0.8:
                df[col] = df[col].astype(str).str.replace(r"^[a-zA-Z]+", "", regex=True)
                logger.info(f"🔧 Coluna '{col}' tratada: prefixo de letras removido")
