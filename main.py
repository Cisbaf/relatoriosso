import schedule
import time
from dotenv import load_dotenv
import os
from src.repository.bigquery import BigQueryRepository
from datetime import date, timedelta
from src.infra.celeryapp.app import task_sso

load_dotenv(override=True)

def update_relatorios():
    url = os.getenv("URL")
    project_id = os.getenv("PROJECTID")
    table_id = os.getenv("TABLEID")
    big_query = BigQueryRepository(project_id=project_id, table_id=table_id)
    date_atual = date.today()
    last_update = big_query.get_last_insert()
    diference = (date_atual - last_update).days
    if diference < 4:
        return
    start_date = last_update + timedelta(days=1)
    end_date = last_update + timedelta(days=2)
    task_sso.delay(
        start_date.strftime("%d/%m/%Y"),
        end_date.strftime("%d/%m/%Y"),
        url,
        project_id,
        table_id
    )

schedule.every(1).days.at("08:00").do(update_relatorios)

while True:
    schedule.run_pending()
    time.sleep(60)
