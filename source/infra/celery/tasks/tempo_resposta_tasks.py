from source.infra.celery.app import app
from source.infra.relatorios.tempo_resposta import critico, regulacao, tih, processing
from source.infra.sso.controller import SSOController
from dataclasses import dataclass
from source.application.repository.task import Task

@dataclass
class DataTask:
    user: str
    password: str
    url_download: str


@app.task(bind=True)
def task_tempo_resposta(self, data: dict):
    data = DataTask(**data)
    controller = SSOController()
    request = controller.get_request(data.user, data.password, data.url_download)

    analise = processing.TempoRespostaProcessing(relatorios=[
        critico.RelatorioCritico(name="Relatorio Tempo Resposta Critico", request=request),
        regulacao.RelatorioRegulacao(name="Relatorio Tempo Resposta Regulação", request=request),
        tih.RelatorioTIH(name="Relatorio Tempo Resposta TIH", request=request),
    ])

    df_result = analise.processing()


class TaskTempoResposta(Task):

    def __init__(self, intervals_day, hour, url: str, project_id: str, table_id: str):
        super().__init__(intervals_day, hour)
        self.url = url
        self.project_id = project_id
        self.table_id = table_id

    def execute(self):
        pass