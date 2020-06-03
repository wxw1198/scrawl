import re

import threadpool
from bs4 import BeautifulSoup
from utils.request import *
import district
from db.mysql import *


def update(city) -> (int, int):
    lock = threading.Lock()
    houseTotalOfCity = 0
    cityAverage = 0.0
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
    paramList = []

    for i in list:
        list = i.find_all("a")
        for i in list:
            href = i.get("href")
            if len(re.findall(r".*zhoubian", href)) == 0:  # not zhoubian
                pinyin_countryTowns.append(href)
                ch_countryTowns.append(i.get_text())
                group = [city, href, i.get_text()]
                paramList.append(group)
                # (target=run, args=("t1",)
                # t =  threading.Thread(target=req, args=(city,href,i.get_text(),))
                # t.start()
                # t.join()

                # threads.append(t)

    pool = threadpool.ThreadPool(len(paramList))
    requests = threadpool.makeRequests(reqCountryTown, paramList)
    [pool.putRequest(req) for req in requests]
    pool.wait()

    if houseTotalOfCity is not None and houseTotalOfCity != 0:
        AddCity(city, cityAverage / houseTotalOfCity, houseTotalOfCity, url)
        return houseTotalOfCity, cityAverage / houseTotalOfCity
    else:
        print("err contry town:", houseTotalOfCity, cityAverage)
        return 0, 0


def reqCountryTown(params):
    global houseTotalOfCity
    global cityAverage
    global lock

    city = params[0]
    href = params[1]
    contryTownName = params[2]

    try:
        totalNumOfHouse, areaAverage = district.update(city, href)
        if totalNumOfHouse is None or totalNumOfHouse == 0:
            print(href, city, totalNumOfHouse, areaAverage)
            return
    except  Exception as e:
        print("district update exception:", e, "city:", city, "href:", href)
        return

    print("country town:", href, contryTownName, "total house:", totalNumOfHouse, "areaAverage:", areaAverage)

    lock.acquire()
    houseTotalOfCity += totalNumOfHouse
    cityAverage += areaAverage * totalNumOfHouse
    lock.release()
    AddCountryTown(contryTownName, areaAverage, totalNumOfHouse, href)


if __name__ == '__main__':
    db_init()
    t, t1 = update("sh")
    print("house num:", t, t1)
