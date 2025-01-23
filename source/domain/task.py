from dataclasses import dataclass


@dataclass
class DataTask:
    user: str
    password: str
    url_download: str
    project_id: str
    table_id: str
    date_in: str
    date_fim: str
