from abc import ABC, abstractmethod
from src.helper.data import Date
import pandas as pd


class RelatorioRepository(ABC):

    def __init__(self, name, principal=False):
        self.name = name
        self.principal = principal
        self.df: pd.DataFrame = None
    
    def load_df(self, df: pd.DataFrame):
        self.df = df

    def export(self, path):
        self.df.to_excel(f'{path}/{self.name.replace(" ", "").lower()}.xlsx', index=False)

    def trate(self, drop_total=True):
        column_names = self.df.iloc[2]
        self.df = self.df[3:]
        self.df.columns = column_names
        if drop_total:
            if 'TOTAL' in self.df.columns:
                self.df = self.df.drop('TOTAL', axis=1)
        self.df = self.df.reset_index(drop=True)

    @abstractmethod
    def payload(self, start: Date, end: Date) -> str:
        raise NotImplemented