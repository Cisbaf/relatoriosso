from typing import List
from abc import ABC, abstractmethod
from source.domain.relatorio import Relatorio
import pandas as pd

class DataProcessing(ABC):

    def __init__(self, relatorios: List[Relatorio]):
        self.df_principal: pd.DataFrame = None
        self.dfs = {}
        self.relatorios = relatorios
        for relatorio in relatorios:
                if relatorio.principal:
                    self.df_principal = relatorio.df
                else:
                    self.dfs[relatorio.name] = relatorio.df

    @abstractmethod
    def processing(self) -> pd.DataFrame:
        raise NotImplementedError