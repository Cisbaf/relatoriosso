from dataclasses import dataclass


@dataclass
class Date:
    day: str
    month: str
    year: str

    def convert_date(self) -> str:
        return f'{self.day}%2F{self.month}%2F{self.year}'
    
    
    @classmethod
    def split(cls, date: str):
        date_split = date.split('/')
        return Date(date_split[0], date_split[1], date_split[2])