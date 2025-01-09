from src.repository.sso import SSOCONTROLLER
from src.helper.coockie import Coockies
from src.helper.relatorio_request import RelatorioRequest
from src.helper.relatorio_list import RelatorioList
from src.helper.analise import DataProcessing
from src.repository.bigquery import BigQueryRepository
from src.helper.data import Date
from src.infra import payloads
from celery import Celery


app = Celery('tasks', broker='redis://redis:6379/0')
app.conf.result_backend = 'redis://redis:6379/0'
app.conf.timezone = 'UTC'

@app.task(bind=True, name="Task_sso_automate")
def task_sso(self, start_date: str, end_date: str, url: str, project_id: str, table_id: str):

    # selenium automate sso
    sso = SSOCONTROLLER()
    sso.login("DANIEL.FERNANDES", "42658265")
    coockies = Coockies.get(sso.get_coockies())
    sso.driver.quit()

    # request api sso
    _start_date = Date.split(start_date)
    _end_date = Date.split(end_date)
    relatorio_request = RelatorioRequest(
        asp_session_id=coockies.asp_session,
        tr_acesso=coockies.tr_acess,
        auto_coockie=coockies.auto_coockie,
    )
    relatorio_list = RelatorioList()
    for relatorio in relatorio_list.get_relatorios():
        relatorio.load_df(relatorio_request.get_relatorio(url, relatorio.payload(_start_date, _end_date)))
        relatorio.trate()

    # tratar dados
    analise = DataProcessing(relatorio_list.relatorios)
    analise.join()

    #big query
    df_bigquery, last_date = analise.treat_for_bigquery()
    big_query = BigQueryRepository(project_id=project_id, table_id=table_id)
    big_query.insert_data(df_bigquery, last_date)

    return "Processo concluído com sucesso"
