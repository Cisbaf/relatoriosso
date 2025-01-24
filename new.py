import schedule
import time
from dotenv import load_dotenv
import os
from source.infra.celery.tasks.analitico_tasks import TaskAnalitico


time.sleep(30)
load_dotenv(override=True)

url = os.getenv("URL")
project_id = os.getenv("PROJECTID")
table_id = os.getenv("TABLEID")
user = os.getenv("USER")
password = os.getenv("PASSWORD")

analitico = TaskAnalitico(
    intervals_day=None,
    hour=None,
    url_download=url,
    project_id=project_id,
    table_id=table_id,
    user=user,
    password=password
)

analitico.execute()

while True:
    time.sleep(60)