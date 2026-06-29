from pathlib import Path
from loguru import logger
from src.config import FileConfig

import pandas as pd


class FileLoader:
    def __init__(self, config: FileConfig):
        self.config = config

    def _read_csv(self, path: Path) -> pd.DataFrame:
        """
        Lê um arquivo CSV detectando automaticamente o delimitador.

        Testa os delimitadores [',', ';'] em ordem. O primeiro que gerar um DataFrame
        com mais de uma coluna é considerado o correto.

        Args:
            path (Path): Caminho do arquivo CSV a ser lido.

        Returns:
            pd.DataFrame: DataFrame carregado com o delimitador correto.

        Raises:
            ValueError: Se nenhum dos delimitadores testados conseguir ler o arquivo.
        """
        logger.info(f"🕵🏻 Detectando delimitador do arquivo '{path}'")
        for delimiter in [",", ";"]:
            try:
                df: pd.DataFrame = pd.read_csv(
                    path,
                    delimiter=delimiter,
                    encoding=self.config.encoding,
                    low_memory=False,
                )
                if len(df) > 1:
                    logger.success(f"✅ Delimitador encontrado: '{delimiter}'")
                    return df

            except Exception:
                continue

        raise ValueError(f"❌ Não foi possível detectar o delimitador de '{path.name}'")

    def load(self) -> pd.DataFrame:
        """
        Carrega um arquivo e retorna um DataFrame.

        Detecta a extensão do arquivo e delega para o método de leitura correto.

        Returns:
            pd.DataFrame: DataFrame carregado com os dados do arquivo.

        Raises:
            FileNotFoundError: Se o arquivo não existir no caminho informado.
            ValueError: Se a extensão do arquivo não for suportada.
        """
        try:
            path: Path = Path(self.config.file_path)

            if not path.exists():
                raise FileNotFoundError(f"⚠️ Arquivo '{path}' não encontrado")

            if path.suffix == ".csv":
                df: pd.DataFrame = self._read_csv(path)
                info: str = f"""📤 Arquivo '{path}' carregado:
                {len(df)} linhas | {len(df.columns)} colunas"""
                logger.success(info)
                return df

        except FileNotFoundError as err:
            logger.error(err)
