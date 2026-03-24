from typing import List
import pandas as pd, re, unidecode
from source.domain.relatorio import Relatorio

def clean_column_name(name):
    name = unidecode.unidecode(name)  # Remove acentos
    name = re.sub(r'\s+', '_', name)  # Substitui espaços por underlines
    name = re.sub(r'[^\w\s]', '', name)  # Remove caracteres especiais
    return name

def extrair_numero(x):
    match = re.search(r'\d+', str(x))
    return match.group() if match else x

class TempoRespostaProcessingMerge:

    def __init__(
        self,
        relatorios_analiticos: List = None,
        relatorios_acrescentar: List = None,
        make=True
    ):
        self.df_analiticos = {}
        self.df_acrescentar = {}

        if make:
            for r in relatorios_analiticos:
                if r.df is not None:
                    self.df_analiticos[r.name] = r.df.copy()

            for r in relatorios_acrescentar:
                if r.df is not None:
                    self.df_acrescentar[r.name] = r.df.copy()

    def processing(self):
        search = 'CÓDIGO DO CHAMADO'

        # 🔹 1. Junta os analíticos
        df_final = pd.concat(self.df_analiticos.values(), ignore_index=True)

        # 🔹 2. Normaliza chave de busca
        df_final['CHAMADO'] = df_final['CHAMADO'].apply(extrair_numero)

        # 🔹 3. Faz merge com cada DF de complemento
        for sub_df in self.df_acrescentar.values():

            sub_df = sub_df.copy()
            sub_df[search] = sub_df[search].apply(extrair_numero)

            # Remove colunas indesejadas
            cols_validas = [c for c in sub_df.columns if c not in ['TOTAL', search]]

            # 🔥 merge
            df_final = df_final.merge(
                sub_df[[search] + cols_validas],
                how='left',
                left_on='CHAMADO',
                right_on=search
            )

            # remove coluna duplicada da chave
            df_final.drop(columns=[search], inplace=True)

        # 🔹 4. Preenche valores não encontrados
        df_final.fillna("#N/A", inplace=True)

        # 🔹 5. Ordenação final
        columns_order = [
            "TIPO CHAMADO", "PRIORIDADE (CHAMADO)", "CIDADE", "CHAMADO", "DIGÍTO",
            "INÍCIO TARM", "FIM TARM", "TEMPO TARM", "TARM",
            "INÍCIO REGULAÇÃO", "FIM REGULAÇÃO", "TEMPO REGULAÇÃO",
            "MÉDICO REGULADOR", "INÍCIO OPERADOR", "SOLICITAÇÃO VTR",
            "TEMPO OPERADOR", "RÁDIO OPERADOR", "EMPENHO VTR", "SAÍDA VTR",
            "CHEGADA AO LOCAL", "TEMPO VTR", "LIBERAÇÃO VTR",
            "TEMPO OCUPAÇÃO", "VTR", "TEMPO RESPOSTA",
            "EQUIPE EMBARCADA", "TEMPO MÉDIO DESLOCAMENTO LOCAL AO HOSPITAL", "HD"
        ]

        df_final = df_final[[c for c in columns_order if c in df_final.columns]]

        return df_final
    
    def treat_for_bigquery(self, df: pd.DataFrame):
        # 🔹 limpa nomes das colunas
        df.columns = [clean_column_name(col) for col in df.columns]

        # 🔹 converte número
        if 'DIGITO' in df.columns:
            df['DIGITO'] = pd.to_numeric(df['DIGITO'], errors='coerce')

        # 🔹 lista de colunas de data
        datetime_cols = [
            'INICIO_TARM', 'FIM_TARM',
            'INICIO_REGULACAO', 'FIM_REGULACAO',
            'INICIO_OPERADOR', 'SOLICITACAO_VTR',
            'EMPENHO_VTR', 'SAIDA_VTR',
            'CHEGADA_AO_LOCAL', 'LIBERACAO_VTR'
        ]

        # 🔥 conversão vetorizada segura
        for col in datetime_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(
                    df[col],
                    format='%d/%m/%Y %H:%M:%S',
                    errors='coerce'  # não quebra o pipeline
                )

        # 🔹 última data
        last_date = df['INICIO_TARM'].max() if 'INICIO_TARM' in df.columns else None

        return df, last_date


