from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Coockies:
    auto_coockie: str
    tr_acess: str
    asp_session: str

    @classmethod
    def get(cls, coockie: List[Dict]):
        # Mapeia os cookies relevantes pelos nomes
        auto_cookie_value = next((c['value'] for c in coockie if c['name'] == 'AutoCookie'), None)
        tr_acess_value = next((c['value'] for c in coockie if c['name'] == 'TrAcesso'), None)
        asp_session_value = next((c['value'] for c in coockie if c['name'] == 'ASP.NET_SessionId'), None)

        # Verifica se todos os valores necessários foram encontrados
        if auto_cookie_value is None or tr_acess_value is None or asp_session_value is None:
            raise ValueError("Um ou mais cookies obrigatórios estão ausentes.")

        # Retorna a instância da classe preenchida
        return cls(
            auto_coockie=auto_cookie_value,
            tr_acess=tr_acess_value,
            asp_session=asp_session_value
        )