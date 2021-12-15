from pet import Pet,Gender
from breed import Breed

from sqlite_helper import DbManager


if __name__ == "__main__":
    DbManager.init_tables()
    
    d = Breed("Berger Créole")    
    print(d.get_id())
    p = Pet("Prada", "20181025", Gender.FEMALE, d)
    p.save()
