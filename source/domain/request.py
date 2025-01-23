from dataclasses import dataclass
import requests
from source.domain.date import Date
from source.domain.coockie import Coockie

@dataclass
class Request:
    url: str
    coockie: Coockie
    date_in: Date
    date_fim: Date
    
    def __get_header__(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie':  f"IDCidade=6994; IDEstabelecimento=0; IDUsuario=1392; NomeUsuario=DANIEL FERNANDES PEREIRA; NivelUsuario=4; Ramal=; IdAgente=; ASP.NET_SessionId={self.coockie.asp_session_id}; TrAcesso={self.coockie.tr_acess}; AutoCookie={self.coockie.auto_coockie}"
        }
    
    def get(self, payload) -> requests.Response:
        return requests.post(
            self.url,
            headers=self.__get_header__(),
            data=payload
        )
    