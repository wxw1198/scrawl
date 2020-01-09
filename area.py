import os
from typing import List
from bs4 import BeautifulSoup
import village
from utils.request import *


# from utils.log import *
def update(city, disctrict) -> (int, int):
    # return pinyin_area ch_area disctrictTotalNum disctrictAverage

    # get areas
    url = "https://{}.lianjia.com/{}".format(city, disctrict)

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
        return None, None, None, None

    areasList = list[1]

    disctrictTotal = 0
    disctrictAverage = 0
    csv_file = os.getcwd() + "/{0}_{1}.csv".format(city, disctrict)
    with open(csv_file, "w") as f:
        for i in areasList.find_all("a"):
            href = i.get("href")
            area_totalnum, area_average = village.update(city, href)
            if area_totalnum is not None:
                pinyin_areas.append(href)

                disctrictTotal += int(area_totalnum)
                disctrictAverage += int(area_average) * area_totalnum

                cn_areas.append(i.get_text())
                # print(i.get("href"))
                # print(i.get_text())

                print(i.get_text(), area_totalnum, area_average)
                f.write(href, i.get_text, area_totalnum, area_average)

    # print("area", url, disctrictTotal, int(area_average / disctrictTotal), "yuan/pingmi")
    print("in {0} have {1} houses, average {} yuan/pingmi".format(disctrict, disctrictTotal,
                                                                  int(area_average / disctrictTotal)))
    return disctrictTotal, int(area_average / disctrictTotal)


if __name__ == '__main__':
    _, _, t = update("sh", "ershoufang/pudong")
    print("house num:", t)
