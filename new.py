import time
from dotenv import load_dotenv
import os
from source.infra.sso.controller import SSOController
from source.domain.request import Request
from source.domain.date import Date
from source.infra.relatorios.tempo_resposta import processing, critico

from source.infra.bigquery.big import BigQueryRepository

time.sleep(30)
load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
table_id = os.getenv("TABLEID")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

coockie = SSOController("Daniel.Fernandes", "42658265", "http://localhost:4444/wd/hub").get_coockie()

request = Request(
    url="https://cisbaf.ssosamu.com:3001/SSONovaIguacu/_Relatorio/frmConsultaRelatorioNovo.aspx",
    coockie=coockie,
    date_in=Date.split("01/01/2024"),
    date_fim=Date.split("30/12/2024")
)

analise = processing.TempoRespostaProcessing(relatorios=[
    critico.RelatorioCritico(name="Critico", request=request),
])

relatorio = analise.relatorios[0]

print(len(relatorio.df))