from source.infra.celery.app import app
from source.domain.date import Date
from source.infra.sso.controller import SSOController
from source.domain.request import Request
from source.domain.task import DataTask
from source.infra.relatorios.analitico import (
    critico, destino, diaxhorario, one, processing,regulacao, three, tih, total_envios, two
)
from source.infra.bigquery.big import BigQueryRepository
from source.application.repository.task import Task
from datetime import date, timedelta


@app.task(bind=True)
def task_relatorio_analitico(self, data: DataTask):
    data = DataTask(**data)
    
    coockie = SSOController(data.user, data.password).get_coockie()
    print(data.date_in)
    request = Request(
        url=data.url_download,
        coockie=coockie,
        date_in=Date.split(data.date_in),
        date_fim=Date.split(data.date_fim)
    )

    analise = processing.AnaliticoProcessing(relatorios=[
        critico.AnaliticoCritico(name="Critico", request=request),
        regulacao.AnaliticoRegulacao(name="Regulação", request=request),
        tih.AnaliticoTIH(name="TIH", request=request),
        one.ChamadosOne(name="Chamado PT 1", request=request, principal=True),
        two.ChamadosTwo(name="Chamado PT 2", request=request),
        three.ChamadosThree(name="Chamado PT 3", request=request),
        destino.DestinoPaciente(name="Destino Paciente", request=request),
        diaxhorario.DiaXHorario(name="Dia X Horario", request=request),
        total_envios.TotalEnvios(name="Total ENvios", request=request)
    ])

    big = BigQueryRepository(
        project_id=data.project_id,
        table_id=data.table_id
    )

    df, last = analise.treat_for_bigquery(
            df=analise.reform(df=analise.processing())
        )
    
    big.insert_data(df, last)

class TaskAnalitico(Task):

    def __init__(self, intervals_day: int, hour: str, url_download: str, project_id: str, table_id: str, user: str, password: str):
        super().__init__(intervals_day, hour)
        self.url_download = url_download
        self.project_id = project_id
        self.table_id = table_id
        self.user = user
        self.password = password
        self.task = task_relatorio_analitico

    def execute(self):
        big_query = BigQueryRepository(project_id=self.project_id, table_id=self.table_id)
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
            "url_download": self.url_download,
            "project_id": self.project_id,
            "table_id": self.table_id,
            "date_in": data_in.strftime("%d/%m/%Y"),
            "date_fim": data_fim.strftime("%d/%m/%Y"),
        })
