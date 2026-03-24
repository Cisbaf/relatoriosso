from typing import List
import pandas as pd, re, unidecode
from source.domain.relatorio import Relatorio

def clean_column_name(name):
    name = unidecode.unidecode(name)  # Remove acentos
    name = re.sub(r'\s+', '_', name)  # Substitui espaços por underlines
    name = re.sub(r'[^\w\s]', '', name)  # Remove caracteres especiais
    return name

class TempoRespostaProcessing:

    def __init__(self,
        relatorios_analiticos: List[Relatorio] = None,
        relatorios_acrescentar: List[Relatorio] = None,
        make=True
        ):
        self.df_analiticos = {}
        self.df_acrestencar = {}
        if make:
            for r_analiticos in relatorios_analiticos:
                if r_analiticos.df is None:
                    continue  # ignora esse relatório
                self.df_analiticos[r_analiticos.name] = r_analiticos.df
            for r_acrescentar in relatorios_acrescentar:
                if r_acrescentar.df is None:
                    continue  # ignora esse relatório
                self.df_acrestencar[r_acrescentar.name] = r_acrescentar.df

    def processing(self):
        search = 'CÓDIGO DO CHAMADO'
        exclude = ['TOTAL', search]
        df_final = pd.concat(self.df_analiticos.values(), ignore_index=True)
        
        for sub_df in self.df_acrestencar.values():
            for name_col in sub_df.columns.values:
                if name_col not in exclude:
                    df_final[name_col] = ''

        shape = df_final.shape[0]
        for i in range(shape):
            cod_chamado = df_final.at[i, 'CHAMADO']
            for sub_df in self.df_acrestencar.values():
                index_linha = sub_df[
                    sub_df[search]
                    .astype(str)
                    .str.contains(str(cod_chamado), regex=False, na=False)
                ].index
                
                for name_col in sub_df.columns.values:
                    if name_col not in exclude:
                        if not index_linha.empty:
                            match_index = index_linha[0]
                            value = sub_df.at[match_index, name_col]
                            df_final.at[i, name_col] = value
                        else:
                            df_final.at[i, name_col] = "#N/A"
        columns_order = [
            "TIPO CHAMADO", "PRIORIDADE (CHAMADO)", "CIDADE", "CHAMADO", "DIGÍTO", "INÍCIO TARM", "FIM TARM", "TEMPO TARM", "TARM", "INÍCIO REGULAÇÃO", "FIM REGULAÇÃO",
            "TEMPO REGULAÇÃO", "MÉDICO REGULADOR", "INÍCIO OPERADOR", "SOLICITAÇÃO VTR", "TEMPO OPERADOR", "RÁDIO OPERADOR", "EMPENHO VTR", "SAÍDA VTR",
            "CHEGADA AO LOCAL", "TEMPO VTR", "LIBERAÇÃO VTR", "TEMPO OCUPAÇÃO", "VTR", "TEMPO RESPOSTA", "EQUIPE EMBARCADA", "TEMPO MÉDIO DESLOCAMENTO LOCAL AO HOSPITAL", "HD"
        ]

        columns_check = [col for col in columns_order if col in df_final.columns]
        
        df_final = df_final[columns_check]

        return df_final
    
    def treat_for_bigquery(self, df: pd.DataFrame):
        df.columns = [clean_column_name(col) for col in df.columns]

        df['DIGITO'] = pd.to_numeric(df['DIGITO'], errors='coerce')

        df['INICIO_TARM'] = pd.to_datetime(
            df['INICIO_TARM'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['FIM_TARM'] = pd.to_datetime(
            df['FIM_TARM'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['INICIO_REGULACAO'] = pd.to_datetime(
            df['INICIO_REGULACAO'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['FIM_REGULACAO'] = pd.to_datetime(
            df['FIM_REGULACAO'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['INICIO_OPERADOR'] = pd.to_datetime(
            df['INICIO_OPERADOR'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['SOLICITACAO_VTR'] = pd.to_datetime(
            df['SOLICITACAO_VTR'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['EMPENHO_VTR'] = pd.to_datetime(
            df['EMPENHO_VTR'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['SAIDA_VTR'] = pd.to_datetime(
            df['SAIDA_VTR'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['CHEGADA_AO_LOCAL'] = pd.to_datetime(
            df['CHEGADA_AO_LOCAL'],
            format='%d/%m/%Y %H:%M:%S'
        )

        df['LIBERACAO_VTR'] = pd.to_datetime(
            df['LIBERACAO_VTR'],
            format='%d/%m/%Y %H:%M:%S'
        )

        last_date = df['INICIO_TARM'].max()

        return df, last_date



