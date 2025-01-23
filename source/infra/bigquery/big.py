from google.cloud import bigquery
from google.oauth2 import service_account
from pandas_gbq import to_gbq
from datetime import datetime, timezone


class BigQueryRepository:

    def __init__(self, project_id, table_id):
        self.project_id = project_id
        self.table_id = table_id
        self.credentials = service_account.Credentials.from_service_account_file(
            'client.json',
            scopes=['https://www.googleapis.com/auth/bigquery']
        )
        self.client = bigquery.Client(credentials=self.credentials, project=self.project_id) #'integracaosheets-426313'

    def insert_data(self, df, last):
        to_gbq(df,
            destination_table=self.table_id, #'integracaosheets-426313.Portal_SAMU.Base 2024'
            project_id=self.project_id,
            if_exists='append',
            credentials=self.credentials
        )

        # Atualizar a tabela Data Atualização
        dt_atualizacao = datetime.now(timezone.utc).strftime('%Y-%m-%d')
        query = f"""
        UPDATE `integracaosheets-426313.Portal_SAMU.Data Atualização`
        SET Dt_Atualizacao = DATE('{dt_atualizacao}'), 
            Dt_Registro = DATE('{last}')
        WHERE TRUE -- Atualiza sempre a única linha existente
        """

        # Executar a query
        query_job = self.client.query(query)
        query_job.result() 


    def get_last_update(self):
        query = f"""
            SELECT Dt_Atualizacao FROM `integracaosheets-426313.Portal_SAMU.Data Atualização`
        """
        query_job = self.client.query(query)
        for row in query_job.result():
            date = row[0]
            return date
        
    def get_last_insert(self):
        query = f"""
            SELECT Dt_Registro FROM `integracaosheets-426313.Portal_SAMU.Data Atualização`
        """
        query_job = self.client.query(query)
        for row in query_job.result():
            date = row[0]
            return date
        