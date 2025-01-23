from abc import ABC, abstractmethod
from source.domain.date import Date
from source.domain.request import Request
import pandas as pd, io


class Relatorio(ABC):

    def __init__(self, name:str, request: Request, principal=False):
        self.name = name
        self.request = request
        self.principal = principal
        self.df: pd.DataFrame = None
        self.__make__()

    def __make__(self):
        response = self.request.get(self.payload(self.request.date_in, self.request.date_fim))
        if not response.ok:
            raise Exception("Não foi possivel")
        self.df = self.adjusts(pd.read_html(io.StringIO(response.text))[0])
        print(f"{self.name} construído")

    @abstractmethod
    def adjusts(self, df: pd.DataFrame) -> pd.DataFrame:
        return df

    @abstractmethod
    def payload(self, data_in: Date, data_fim: Date) -> str:
        raise NotImplementedError


