import os
from typing import List
from bs4 import BeautifulSoup
import village
from utils.request import *
from db.mysql import *


# from utils.log import *
def update(city, disctrict) -> (int, int):
    # return pinyin_area ch_area disctrictTotalNum disctrictAverage
    # get areas
    url = "https://{}.lianjia.com/{}".format(city, disctrict)

    html = reqPage(url)
    soup = BeautifulSoup(html, "html.parser")
    list = soup.find_all('div', attrs={'data-role': 'ershoufang'})

    cn_areas = []
    pinyin_areas = []
    i = list[0]

    list = i.find_all("div")
    if len(list) != 2:
        # logger.error("get page err")
        return None, None, None, None

    areasList = list[1]

    disctrictTotal = 0
    disctrictAverage = 0

    filename = disctrict
    filename = filename.replace("/", "_")
    csv_file = os.getcwd() + "/result/{0}_{1}.csv".format(city, filename)
    #with open(csv_file, "w") as f:
    for i in areasList.find_all("a"):
        href = i.get("href")
        area_totalnum, area_average = village.update(city, href)
        if area_totalnum is not None:
            pinyin_areas.append(href)

            disctrictTotal += int(area_totalnum)
            disctrictAverage += int(area_average) * area_totalnum
            cn_areas.append(i.get_text())

            AddDistrict(filename,area_average,area_totalnum,href)
            #print(i.get_text(), area_totalnum, area_average)
            #write_str = href + "," + i.get_text() + "," + str(area_totalnum) + "," + str(area_average) + "\n"
                # f.write(write_str)
                # f.flush()

    if disctrictTotal != 0 :
    # print("area", url, disctrictTotal, int(area_average / disctrictTotal), "yuan/pingmi")
        print("in {0} have {1} houses, average {2} yuan/pingmi".format(disctrict, disctrictTotal,
                                                                   int(disctrictAverage / disctrictTotal)))
        return disctrictTotal, int(disctrictAverage / disctrictTotal)
    else :
        print("err:",url)
        return  0,0



if __name__ == '__main__':
    db_init()
    _, _, total, average = update("wh")
    print("house total num:", total, "average:", average, "in wuhan city")
