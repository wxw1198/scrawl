from bs4 import BeautifulSoup
import village
from utils.request import *


# from utils.log import *

def update(disctrict):
    # get areas
    url = "https://sh.lianjia.com/{}".format(disctrict)

    html = reqPage(url)
    soup = BeautifulSoup(html, "lxml")
    list = soup.find_all('div', attrs={'data-role': 'ershoufang'})

    cn_areas = []
    pinyin_areas = []

    print(len(list))
    print(type(list))
    i = list[0]

    list = i.find_all("div")
    if len(list) != 2:
        # logger.error("get page err")
        return

    areasList = list[1]

    disctrictTotal = 0
    for i in areasList.find_all("a"):
        href = i.get("href")
        area_totalnum, area_average = village.update(href)
        if area_totalnum is not None:
            pinyin_areas.append(href)

            disctrictTotal += int(area_totalnum)
            cn_areas.append(i.get_text())
            # print(i.get("href"))
            # print(i.get_text())
            print(i.get_text(), area_totalnum, area_average)

    return pinyin_areas, cn_areas, disctrictTotal


if __name__ == '__main__':
    _, _, t = update("ershoufang/pudong")
    print("house num:", t)
