import os
import re
import threading
from bs4 import BeautifulSoup
from utils.request import *
import district
from db.mysql import *

lock = threading.Lock()


houseTotalOfCity = 0
cityAverage = 0.0

def update(city) -> (int, int):
    # fa song qing qiu ,huo qu dao chengshi da quyv ,ranho zai gengxin
    # https://sh.lianjia.com/ershoufang/
    # get all ditricts
    # return totalNumOfHouse average
    url = "https://{}.lianjia.com/ershoufang".format(city)
    html = reqPage(url)

    soup = BeautifulSoup(html, "html.parser")
    list = soup.find_all('div', attrs={'data-role': 'ershoufang'})

    ch_countryTowns = []
    pinyin_countryTowns = []

    #threads = []

    #csv_file = os.getcwd() + "/result/{0}.csv".format(city)
    #with open(csv_file, "w") as f:
    for i in list:
        list = i.find_all("a")
        for i in list:
            href = i.get("href")
            if len(re.findall(r".*zhoubian", href)) == 0:

                pinyin_countryTowns.append(href)
                ch_countryTowns.append(i.get_text())
                #(target=run, args=("t1",)
                t =  threading.Thread(target=req, args=(city,href,i.get_text(),))
                t.start()
                t.join()
                #threads.append(t)


    if houseTotalOfCity is None or houseTotalOfCity != 0:
        AddCity(city, cityAverage / houseTotalOfCity, houseTotalOfCity, url)
        #
        return houseTotalOfCity, cityAverage / houseTotalOfCity

    else :
        print("err contry town:", houseTotalOfCity, cityAverage)


def req(city, href, contryTownName):
    global  houseTotalOfCity
    global  cityAverage
    global lock

    totalNumOfHouse, areaAverage = district.update(city, href)
    if totalNumOfHouse is None or totalNumOfHouse == 0:
        print(href, city, totalNumOfHouse,areaAverage)
        return

    print("country town:", href,contryTownName, "total house:",totalNumOfHouse, "areaAverage:",areaAverage)

    lock.acquire()
    houseTotalOfCity += totalNumOfHouse
    cityAverage += areaAverage * totalNumOfHouse
    lock.release()
    AddCountryTown(contryTownName, areaAverage, totalNumOfHouse, href)


if __name__ == '__main__':
   db_init()
   t,t1 = update("sh")
   print("house num:", t,t1)