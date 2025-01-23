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

class MockTask(TaskAnalitico):

    def execute(self):
        self.task.delay({
            "user": self.user,
            "password": self.password,
            "url_download": self.url_download,
            "project_id": self.project_id,
            "table_id": self.table_id,
            "date_in": "05/01/2025",
            "date_fim": "20/01/2025"
        })

analitico = MockTask(
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