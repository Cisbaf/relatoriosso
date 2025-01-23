from source.domain.relatorio import Relatorio


class RelatorioAnalitico(Relatorio):

    def adjusts(self, df, drop_total=True):
        column_names = df.iloc[2]
        df = df[3:]
        df.columns = column_names
        if drop_total:
            if 'TOTAL' in df.columns:
                df = df.drop('TOTAL', axis=1)
        df = df.reset_index(drop=True)
        return df
    
    def payload(self, data_in, data_fim):
        return super().payload(data_in, data_fim)