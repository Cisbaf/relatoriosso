from source.infra.celery.app import app
from source.domain.date import Date
from source.infra.sso.controller import SSOController
from source.domain.request import Request
from source.domain.task import DataTask
from source.infra.relatorios.tempo_resposta import regulacao, critico, tih, total_chamados, destino, processingmerge
from source.infra.bigquery.big import BigQueryRepository
from source.application.repository.task import Task
from datetime import date, timedelta


@app.task(bind=True)
def task_relatorio_tempo_resposta(self, data: DataTask):
    data = DataTask(**data)
    
    coockie = SSOController(data.user, data.password, data.url_base).get_coockie()

    request = Request(
        url=f"{data.url_base}/_Relatorio/frmConsultaRelatorioNovo.aspx",
        coockie=coockie,
        date_in=Date.split(data.date_in),
        date_fim=Date.split(data.date_fim)
    )

    process = processingmerge.TempoRespostaProcessingMerge(
        relatorios_analiticos=[
            regulacao.RelatorioRegulacao("Regulação", request=request),
            critico.RelatorioCritico("Critico", request=request),
            tih.RelatorioTIH("TIH", request=request)
        ],
        relatorios_acrescentar=[
            total_chamados.RelatorioTotalChamados("total chamados", request=request),
            destino.RelatorioDestino("Destino", request=request)
        ]
    )

    df, last = process.treat_for_bigquery(process.processing())

    big = BigQueryRepository(
        project_id=data.project_id,
        table_id=data.table_id,
        table_dt=data.table_update_id
    )

    big.insert_data(df, last)
    

class TaskTempoResposta(Task):

    def __init__(self, intervals_day: int, hour: str, url_base: str, project_id: str, table_id: str, table_update_id: str, user: str, password: str):
        super().__init__(intervals_day, hour)
        self.url_base = url_base
        self.project_id = project_id
        self.table_id = table_id
        self.table_update_id = table_update_id
        self.user = user
        self.password = password
        self.task = task_relatorio_tempo_resposta

    def execute(self):
        big_query = BigQueryRepository(project_id=self.project_id, table_id=self.table_id, table_dt=self.table_update_id)
        date_atual = date.today()
        last_update = big_query.get_last_insert()
        diference = (date_atual - last_update).days
        if diference < 4:
            return
        data_in: date = last_update + timedelta(days=1)
        data_fim: date = last_update + timedelta(days=2)
        self.task.delay({
            "user": self.user,
            "password": self.password,
            "url_base": self.url_base,
            "project_id": self.project_id,
            "table_id": self.table_id,
            "table_update_id": self.table_update_id,
            "date_in": data_in.strftime("%d/%m/%Y"),
            "date_fim": data_fim.strftime("%d/%m/%Y"),
        })
