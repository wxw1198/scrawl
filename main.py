import city
from db.mysql import *

def update():
    db_init()
    city.update()

#city --> area  --->distict --> village

if __name__ == "__main__":
    update()