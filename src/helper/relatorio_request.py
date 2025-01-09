from dataclasses import dataclass
from src.helper.data import Date
import pandas as pd, requests, io


@dataclass
class RelatorioRequest:
    asp_session_id: str
    tr_acesso: str
    auto_coockie: str

    def get_header(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie':  f"IDCidade=6994; IDEstabelecimento=0; IDUsuario=1392; NomeUsuario=DANIEL FERNANDES PEREIRA; NivelUsuario=4; Ramal=; IdAgente=; ASP.NET_SessionId={self.asp_session_id}; TrAcesso={self.tr_acesso}; AutoCookie={self.auto_coockie}"
        }
    
    def request(self, url, payload):
        return requests.post(url, headers=self.get_header(), data=payload)
    
    def convert_hmtl_data(self, df_str: str):
        return pd.read_html(io.StringIO(df_str))[0]
    
    def get_relatorio(self, url, payload):
        response = self.request(url, payload)
        if response.ok:
            return self.convert_hmtl_data(response.text)
        raise Exception("Problema ao baixar relatorio", response.text)