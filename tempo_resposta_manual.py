from dotenv import load_dotenv
import os
from source.infra.sso.controller import SSOController
from source.domain.request import Request
from source.domain.date import Date
from source.infra.relatorios.tempo_resposta.processing import TempoRespostaProcessing
from source.infra.relatorios.tempo_resposta.processingmerge import TempoRespostaProcessingMerge
from source.infra.relatorios.tempo_resposta import regulacao, critico, tih, destino, total_chamados
from source.infra.bigquery.big import BigQueryRepository


load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
database_id = os.getenv("DATABASEID")
# TEMPO RESPOSTA
tempo_resposta_table_id = os.getenv("TEMPO_RESPOSTA_TABLEID")
tempo_resposta_table_update_id = os.getenv("TEMPO_RESPOSTA_TABLE_UPDATE_ID")
user = os.getenv("USER")
password = os.getenv("PASSWORD")


print("pegando coockie 1/4")
coockie = SSOController(user, password, url, "http://localhost:4444/wd/hub").get_coockie()

request = Request(
    url=f"{url}/_Relatorio/frmConsultaRelatorioNovo.aspx",
    coockie=coockie,
    date_in=Date.split("21/03/2026"),
    date_fim=Date.split("21/03/2026")
)

print("fazendo download 2/4")
process = TempoRespostaProcessingMerge(
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

print("processando df 3/4")
df, last = process.treat_for_bigquery(process.processing())

big = BigQueryRepository(
    project_id=project_id,
    table_id=f"{project_id}.{database_id}.{tempo_resposta_table_id}",
    table_dt=f"{project_id}.{database_id}.{tempo_resposta_table_update_id}",
)

print("inserindo no bigquery 4/4")
big.insert_data(df, last)