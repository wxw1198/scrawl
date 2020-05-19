import time
import pymysql


def db_init():
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

    sql = "INSERT INTO cities(cityName,averagePrice,totalNumber,url,timeNow) values(%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (cityName, averagePrice, totalNumber, url, time.strftime("%Y-%m-%d"))),
        db.commit()
    except  Exception as e:
        print("add city:", e)
        db.rollback()


def AddCountryTown(countyTownname, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO countyTowns(countyTownname,averagePrice,totalNumber,url,timeNow) values(%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (countyTownname, averagePrice, totalNumber, url, time.strftime("%Y-%m-%d"))),
        db.commit()
    except  Exception as e:
        print("add country:",e)
        db.rollback()


def AddVillage(villageName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO villages(villageName,averagePrice,count,url,timeNow) values(%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (villageName, averagePrice, totalNumber, url, time.strftime("%Y-%m-%d")))
        db.commit()
    except  Exception as e:
        print("vaillage:", e)
        db.rollback()


def AddHouseInfo(baseInfo, url, priceInfo, positionInfo):
    cursor = db.cursor()

    sql = "INSERT INTO houseInfo(baseInfo,url,priceInfo,positionInfo,timeNow) values(%s,%s,%s,%s,%s)"

   # print(url)
    try:
        cursor.execute(sql, (baseInfo, url, priceInfo, positionInfo, time.strftime("%Y-%m-%d")))
        db.commit()
    except Exception as e:
        print(e)
        print(url)
        db.rollback()


def AddDistrict(districtName, averagePrice, totalNumber, url):
    cursor = db.cursor()

    sql = "INSERT INTO districts(districtName,averagePrice,count ,url,timeNow) values(%s,%s,%s,%s,%s)"
    try:
        cursor.execute(sql, (districtName, averagePrice, totalNumber, url, time.strftime("%Y-%m-%d")))
        db.commit()
    except  Exception as e:
        print("AddDistict:",e)
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
    db_init()
    AddDistrict("111","23","555555","http:2333")