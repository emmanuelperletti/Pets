from datetime import datetime
from breed import Breed
from event import Event
from enum import Enum
from sqlite_helper import Model

class Gender(Enum):
    MALE = 1
    FEMALE = 2

class Pet(Model):
    name: str
    birthdate: datetime
    breed: Breed
    gender: Gender    
    events = []
    table = "pet"
    pk = "id"


    def __init__(self, name:str, birthdate, gender:Gender, breed):
        assert len(name) >= 2
        self.id =-1
        self.name = name
        if type(birthdate) is str:
            self.birthdate = datetime.strptime(birthdate,"%Y%m%d")
        elif type(birthdate) is datetime:
            self.birthdate = birthdate  
        if type(breed) is Breed:
            self.breed = breed
        else:
            self.breed = Breed(breed)
        self.gender = gender
    
    def __str__(self):
        return f"{self.name} ({self.breed.name})"

    def get_insert_statement(self):
        bd = self.birthdate.strftime("%Y%m%d")
        return f"INSERT INTO pet (name,birthdate,gender,breed) VALUES ('{self.name}','{bd}', {self.gender.value}, {self.breed.id} )"

    def get_delete_statement(self):
        return super().get_delete_statement()
    
    def get_update_statement(self):
        return super().get_update_statement()
    
    def get_select_statement(self):
        return super().get_select_statement()

    def add_event(self, event: Event):
        self.events.append(event)


    @property
    def breed_name(self):
        return self.breed.name

    ###WIP
    @classmethod
    def load(cls, key_value):
        if type(key_value) is str:
            operator = 'like'
            key = 'name'
        if type(key_value) is int:
            operator = '='
            key = 'id'
        res = Model.get_by_key(cls.table,key,key_value,operator)
        if res:
            return Pet(res[0]['name'],res[0]['birthdate'], res[0]['gender'], res[0]['breed'])
        else:
            pass
        
    ###ENDWIP