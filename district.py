import re
from bs4 import BeautifulSoup
from utils.request import *
import area


def update(city):
    # fa song qing qiu ,huo qu dao chengshi da quyv ,ranho zai gengxin
    # https://sh.lianjia.com/ershoufang/
    # get all ditricts
    # return ch_districts, en_districts, totalNumOfHouse
    url = "https://{}.lianjia.com/ershoufang".format(city)
    html = reqPage(url)
    soup = BeautifulSoup(html, "lxml")
    list = soup.find_all('div', attrs={'data-role': 'ershoufang'})

    houseTotalOfCity = 0
    cityAverage = 0
    ch_district = []
    pinyin_district = []
    for i in list:
        list = i.find_all("a")
        for i in list:
            href = i.get("href")
            if len(re.findall(r".*zhoubian", href)) == 0:
                pinyin_district.append(href)
                _, _, totalNumOfHouse, areaAverage = area.update(city, href)
                houseTotalOfCity += totalNumOfHouse
                cityAverage += areaAverage * totalNumOfHouse
                ch_district.append(i.get_text)
                print(i.get("href"))
                print(i.get_text())

    return ch_district, pinyin_district, totalNumOfHouse, areaAverage / totalNumOfHouse


if __name__ == '__main__':
    _, _, total, average = update("wh")
    print("house total num:", total, "average:", average, "in wuhan city")
