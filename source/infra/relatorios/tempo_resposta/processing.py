from source.application.repository.processing import DataProcessing
import pandas as pd


class TempoRespostaProcessing(DataProcessing):

    def processing(self):
        columns_orders = ['TIPO CHAMADO', 'PRIORIDADE (CHAMADO)', 'CIDADE', 'CHAMADO', 'DIGÍTO', 'INÍCIO TARM', 'FIM TARM', 'TEMPO TARM', 'TARM', 'INÍCIO REGULAÇÃO', 'FIM REGULAÇÃO', 'TEMPO REGULAÇÃO', 'MÉDICO REGULADOR', 'INÍCIO OPERADOR', 'SOLICITAÇÃO VTR', 'TEMPO OPERADOR', 'RÁDIO OPERADOR', 'EMPENHO VTR', 'SAÍDA VTR',
        'CHEGADA AO LOCAL', 'TEMPO VTR', 'LIBERAÇÃO VTR', 'TEMPO OCUPAÇÃO', 'VTR', 'TEMPO RESPOSTA', 'EQUIPE EMBARCADA']
        
        matching_dfs = [
            df for _, df in self.dfs.items()
            if set(df.columns) == set(columns_orders)
        ]

        if matching_dfs:
            merged_df = pd.concat(matching_dfs, ignore_index=True)
        else:
            merged_df = pd.DataFrame(columns=columns_orders)  # Retorna vazio se não houver correspondência

        return merged_df