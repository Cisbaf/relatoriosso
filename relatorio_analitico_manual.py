from dotenv import load_dotenv
import os
from source.infra.sso.controller import SSOController
from source.domain.request import Request
from source.domain.date import Date
from source.infra.relatorios.analitico import (
    critico, destino, diaxhorario, one, processing,regulacao, three, tih, total_envios, two
)

from source.infra.bigquery.big import BigQueryRepository


load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
database_id = os.getenv("DATABASEID")
# PORTAL SAMU
portal_samu_table_id = os.getenv("PORTAL_SAMU_TABLEID")
portal_samu_table_update_id = os.getenv("PORTAL_SAMU_TABLE_UPDATE_ID")

user = os.getenv("USER")
password = os.getenv("PASSWORD")


print("pegando coockie 1/4")
coockie = SSOController(user, password, url, "http://localhost:4444/wd/hub").get_coockie()

request = Request(
    url=f"{url}/_Relatorio/frmConsultaRelatorioNovo.aspx",
    coockie=coockie,
    date_in=Date.split("11/03/2026"),
    date_fim=Date.split("12/03/2026")
)

print("baixando e tratando dados 2/4 ")
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
    project_id=project_id,
    table_id=f"{project_id}.{database_id}.{portal_samu_table_id}",
    table_dt=f"{project_id}.{database_id}.{portal_samu_table_update_id}",
)

print("tratando dados big query 3/4")
df, last = analise.treat_for_bigquery(
    df=analise.reform(df=analise.processing())
)

print("inserindo dados no bigquery 4/4")
big.insert_data(df, last)
print("finalizado!")
