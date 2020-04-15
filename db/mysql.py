import pymysql


def init():
    global db
    try:
        db = pymysql.connect("127.0.0.1", "root", "123", "houseDB", charset='utf8')

        print("connect mysql ok")

    except:
        print("connect to mysql err")
        exit(-1)


#
def AddCity(cityName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO cities(cityName,averagePrice,totalNumber) values(%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (cityName, averagePrice, totalNumber, url)),
        db.commit()
    except:
        db.rollback()


def AddArea(areaName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO cities(areaName,averagePrice,totalNumber) values(%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (areaName, averagePrice, totalNumber, url)),
        db.commit()
    except:
        db.rollback()


def AddVillage(villageName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO villages(villageName,averagePrice,totalNumber,url) values(%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (villageName, averagePrice, totalNumber, url))
        db.commit()
    except:
        db.rollback()


def AddDistict(distictName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO disticts(distictName,averagePrice,totalNumber,url) values(%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (distictName, averagePrice, totalNumber, url))
        db.commit()
    except:
        db.rollback()

# def ReadDB(name):
#     sql = "SELECT * FROM  values(%s)"
#    cursor = db.cursor()
#
#    try:
#      cursor.execute(sql, (name))
#      data = cursor.fetchone()
#
#       while data:
#         print(data)
#         data = cursor.fetchone()
#     except:
#          print("Error!")


if __name__ == '__main__':
    init()