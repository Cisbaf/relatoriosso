from src.repository.relatorio import RelatorioRepository
from typing import List

class RelatorioList:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RelatorioList, cls).__new__(cls)
            cls._instance._init_once(*args, **kwargs)
        return cls._instance

    def _init_once(self, *args, **kwargs):
        """Inicializa apenas na primeira instância."""
        self.relatorios: List[RelatorioRepository] = []

    def add_relatorio(self, relatorio):
        """Adiciona um relatório à lista."""
        self.relatorios.append(relatorio)

    def get_relatorios(self):
        """Retorna a lista de relatórios."""
        return self.relatorios