import schedule
import time
from dotenv import load_dotenv
import os
from source.infra.celery.tasks.analitico_tasks import TaskAnalitico

load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
table_id = os.getenv("TABLEID")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

TaskAnalitico(
    intervals_day=1,
    hour="08:00",
    url_download=url,
    project_id=project_id,
    table_id=table_id,
    user=user,
    password=password
)

while True:
    schedule.run_pending()
    time.sleep(60)
