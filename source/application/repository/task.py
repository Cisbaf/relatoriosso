from abc import ABC, abstractmethod
import schedule

class Task(ABC):

    def __init__(self, intervals_day: int, hour: str):
        if intervals_day and hour:
            schedule.every(intervals_day).days.at(hour).do(self.execute)
        

    @abstractmethod
    def execute(self):
        raise NotImplementedError

