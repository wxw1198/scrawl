import os
import re
from bs4 import BeautifulSoup
from utils.request import *
import area


def update(city) -> (int, int):
    # fa song qing qiu ,huo qu dao chengshi da quyv ,ranho zai gengxin
    # https://sh.lianjia.com/ershoufang/
    # get all ditricts
    # return totalNumOfHouse average
    url = "https://{}.lianjia.com/ershoufang".format(city)
    html = reqPage(url)
    soup = BeautifulSoup(html, "lxml")
    list = soup.find_all('div', attrs={'data-role': 'ershoufang'})

    houseTotalOfCity = 0
    cityAverage = 0
    ch_district = []
    pinyin_district = []
    csv_file = os.getcwd() + "/{0}.csv".format(city)
    with open(csv_file, "w") as f:
        for i in list:
            list = i.find_all("a")
            for i in list:
                href = i.get("href")
                if len(re.findall(r".*zhoubian", href)) == 0:
                    pinyin_district.append(href)
                    totalNumOfHouse, areaAverage = area.update(city, href)
                    print(href, i.get_text(), totalNumOfHouse, areaAverage)
                    houseTotalOfCity += totalNumOfHouse
                    cityAverage += areaAverage * totalNumOfHouse
                    ch_district.append(i.get_text())
                    write_str = city + "," + i.get_text() + "," + str(totalNumOfHouse) + "," + str(areaAverage) + "\n"
                    f.write(write_str)

    return houseTotalOfCity, cityAverage / houseTotalOfCity


if __name__ == '__main__':
    _, _, total, average = update("wh")
    print("house total num:", total, "average:", average, "in wuhan city")
