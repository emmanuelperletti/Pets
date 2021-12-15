from sqlite_helper import Model, DbManager


class Breed(Model):
    name: str
    all = {}
    
    def __init__(self, key):
        self.table = "breed"
        self.pk = "id"
        self.set_id(-1)
        if type(key) is str:
            self.name = key
            res = self.get_by_name()
            print(res)
            if res:
                self.set_id(res[0][0])
            else:
                self.save()
        elif type(key) is int:
            res = self.get_by_pk(key)
            if res:
                print(res)
                self.name = res[0][0]
                self.set_id(res[0][1])

   

    @classmethod
    def get_all(cls):
        return DbManager.exec("SELECT breed.name, breed.id from breed")

    def get_by_name(self):
        return DbManager.exec(f"SELECT breed.id from breed where breed.name like '{self.name}'")

    def get_insert_statement(self) -> str:
        return f"INSERT INTO breed (name) VALUES ('{self.name}')"

    def get_update_statement(self):
        return f"UPDATE breed set name = '{self.name}' where breed.id = {self.get_id()}"

    def get_delete_statement(self):
        return f"DELETE FROM breed WHERE breed.id = {self.get_id}"

    def get_select_statement(self):
        pass

    
