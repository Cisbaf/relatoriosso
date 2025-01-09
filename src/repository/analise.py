from abc import ABC, abstractmethod
import pandas as pd


class DataProcessingRepository(ABC):
    

    def insert_column(self, df: pd.DataFrame, column):
        df[column] = ''
    
    def order_columns(self, df: pd.DataFrame, columns):
        columns_present = [col for col in columns if col in df.columns]
        return df[columns_present]