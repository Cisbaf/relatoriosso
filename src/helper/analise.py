import pandas as pd, os, re, unidecode
from typing import List
from src.repository.relatorio import RelatorioRepository
from src.repository.analise import DataProcessingRepository


def clean_column_name(name):
    name = unidecode.unidecode(name)  # Remove acentos
    name = re.sub(r'\s+', '_', name)  # Substitui espaços por underlines
    name = re.sub(r'[^\w\s]', '', name)  # Remove caracteres especiais
    return name


class DataProcessing(DataProcessingRepository):

    def __init__(self, relatorios: List[RelatorioRepository]):
        self.dfs = {}
        self.df_principal = None
        if relatorios:
            for relatorio in relatorios:
                if relatorio.principal:
                    self.df_principal = relatorio.df
                else:
                    self.dfs[relatorio.name] = relatorio.df

    def join(self):
        for _, df in self.dfs.items():
            for name_col in df.columns.values:
                if name_col != 'CÓDIGO DO CHAMADO' and name_col != "CHAMADO":
                    self.insert_column(self.df_principal, name_col)

        errors = []
        shape = self.df_principal.shape[0]
        for i in range(shape):
            cod_chamado = self.df_principal.at[i, 'CÓDIGO DO CHAMADO']
            for df_name, df in self.dfs.items():
                try:
                    try:
                        index_linha = df[df['CÓDIGO DO CHAMADO'] == cod_chamado].index
                    except:
                        try:
                            cod_chamado_split = cod_chamado.split('/')[0]
                            index_linha = df[df['CHAMADO'] == cod_chamado_split].index
                        except:
                            pass
                    if not index_linha.empty:
                        match_index = index_linha[0]
                        for col in df.columns:
                            if col != "CÓDIGO DO CHAMADO" and col != "CHAMADO":
                                value = df.at[match_index, col]
                                self.df_principal.at[i, col] = value
                    else:
                        for col in df.columns:
                            if col != "CÓDIGO DO CHAMADO" and col != "CHAMADO":
                                self.df_principal.at[i, col] = "#N/A"
                except Exception as e:
                    errors.append(f"Error processing dataframe {df_name} at index {i}: {e}")

        column_order = [
            'TIPO VTR', 'TIPO HD CHAMADO', 'TIPO CHAMADO', 'SEXO DO PACIENTE',	'PRIORIDADE (CHAMADO)',	'ÓBITO', 'IDADE',
            'IDADE DO PACIENTE', 'CÓDIGO DO CHAMADO', 'CIDADE', 'AÇÃO SEM INTERVENÇÃO', 'TOTAL', 'APH_CRITICO',
            'APH_REGULACAO', 'APH_TIH', 'SUB GRUPO APH CENA', 'PRIORIDADE (CENA)', 'CONDUTA', 'TIPO ESTABELECIMENTO',
            'HOSPITAL',	'PLACA', 'VEÍCULO (BASE)', 'DIA DA SEMANA', 'HORA',	'HD', 'DATA', 'ESTABELECIMENTO ORIGEM',
            'ESTABELECIMENTO', 'ENCERRAMENTO', 'USUÁRIO REGULAÇÃO CHAMADO', 'USUÁRIO ABERTURA CHAMADO'
        ]
        self.df_principal = self.order_columns(self.df_principal, column_order)
        self.df_principal = self.df_principal.iloc[:-1]
        msg_final = f'Gerando relatorio final - Progresso ({shape}/{shape}) 100%'
        if len(errors) > 0:
            raise Exception("Erro encontrado"+errors)
        print(msg_final)
        print("errors:", errors)
        print("quantidade de colunas", len(self.df_principal.columns))
   
    def export(self, path):
        self.df_principal.to_excel(f'{path}/finaldf.xlsx', index=False)

    @classmethod
    def remove_line(cls, df: pd.DataFrame, line) -> pd.DataFrame:
        return df[line:]
    
    
    
    def treat_for_bigquery(self):
        df = self.df_principal
        # Clean column names
        df.columns = [clean_column_name(col) for col in df.columns]

        # Ensure IDADE and TOTAL are cast to integers, handle invalid values by coercing them to NaN
        df['IDADE'] = pd.to_numeric(df['IDADE'], errors='coerce')
        df['TOTAL'] = pd.to_numeric(df['TOTAL'], errors='coerce')
        # Converter a coluna 'data' para o formato datetime
        df['DATA'] = pd.to_datetime(df['DATA'], format='%d/%m/%Y')

        # Se precisar converter para o formato UTC, você pode usar o seguinte
        df['DATA'] = df['DATA'].dt.tz_localize('UTC')

        df['DATA'] = df['DATA'].dt.tz_convert(None)

        last_date = df['DATA'].max()

        return df, last_date
