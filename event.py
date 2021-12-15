from datetime import datetime

class Event:
    name: str
    date: datetime
    reminder: datetime

  
    def __init__(self, name:str, date:str, reminder:str):
       
        
        self.name = name

        if type(date) is str:
            self.date = datetime.strptime(date,"%Y%m%d")
        elif type(date) is datetime:
            self.date = date

        if type(reminder) is str:
            self.reminder = datetime.strptime(reminder,"%Y%m%d")
        elif type(reminder) is datetime:
            self.reminder = reminder
        