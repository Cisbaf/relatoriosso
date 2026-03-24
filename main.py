import schedule, time, os
from dotenv import load_dotenv
from source.infra.celery.tasks.analitico_tasks import TaskAnalitico
from source.infra.celery.tasks.tempo_resposta_tasks import TaskTempoResposta

load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
database_id = os.getenv("DATABASEID")
# PORTAL SAMU
portal_samu_table_id = os.getenv("PORTAL_SAMU_TABLEID")
portal_samu_table_update_id = os.getenv("PORTAL_SAMU_TABLE_UPDATE_ID")
# TEMPO RESPOSTA
tempo_resposta_table_id = os.getenv("TEMPO_RESPOSTA_TABLEID")
tempo_resposta_table_update_id = os.getenv("TEMPO_RESPOSTA_TABLE_UPDATE_ID")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

TaskAnalitico(
    intervals_day=1,
    hour="08:00",
    url_base=url,
    project_id=project_id,
    table_id=f"{project_id}.{database_id}.{portal_samu_table_id}",
    table_update_id=f"{project_id}.{database_id}.{portal_samu_table_update_id}",
    user=user,
    password=password
)

TaskTempoResposta(
    intervals_day=1,
    hour="09:00",
    url_base=url,
    project_id=project_id,
    table_id=f"{project_id}.{database_id}.{tempo_resposta_table_id}",
    table_update_id=f"{project_id}.{database_id}.{tempo_resposta_table_update_id}",
    user=user,
    password=password
)

while True:
    schedule.run_pending()
    time.sleep(60)
