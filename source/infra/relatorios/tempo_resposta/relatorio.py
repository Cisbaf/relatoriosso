from source.domain.relatorio import Relatorio


class RelatorioTempoResposta(Relatorio):

    def adjusts(self, df):
        column_names = df.iloc[2]
        df = df[3:]
        df.columns = column_names
        df = df.reset_index(drop=True)
        return df