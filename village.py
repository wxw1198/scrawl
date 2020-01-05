import re
import time

from utils.request import *
from bs4 import BeautifulSoup


class houseInfo:
    def __init__(self, baseInfo, price, position):
        self.__base__ = baseInfo
        self.__price__ = price
        self.__position__ = position

    def getAveragePrice(self):
        # return 每平米价格，精确到元
        print(self.__base__, self.__price__)
        list = self.__base__.split("|")
        for item in list:

            regex_str = ".*平米.*"
            match_obj = re.match(regex_str, item)

            if match_obj is not None:
                print(match_obj.string)
                strTrip = match_obj.string.strip(" ")

                # 以下是整数和小数正确的正则表达式
                regInt = '^0$|^[1-9]\d*'  # 不接受09这样的为整数
                regFloat = '^[1-9]\d*\.\d+|^[1-9]\d*\.\d+'  # 接受0.00、0.360这样的为小数，不接受00.36，思路:若整数位为零,小数位可为任意整数，但小数位数至少为1位，若整数位为自然数打头，后面可添加任意多个整数，小数位至少1位

                regIntOrFloat = regFloat + '|' + regInt  # 整数或小数

                housingArea = re.search(regIntOrFloat, strTrip)
                housingArea = housingArea.group(0)
                housingAreaInt = housingArea.split(".")[0]

                return 10000 * float(self.__price__) / float(housingAreaInt)

    def getVillageName(self):
        return self.__position__


def update(area):
    # return 总的出售房屋套数 ;map[xiaoqu]housinfo
    url = "https://sh.lianjia.com{}".format(area)
    html = reqPage(url)
    soup = BeautifulSoup(html, "lxml")

    villageHouseInfo = {}

    css_class = soup.find(class_='total fl')
    area_total = css_class.find("span").get_text()

    print(type(area_total))
    area_total = area_total.strip()

    if area_total == "0":
        return None, None

    page_box = soup.find(class_='page-box house-lst-page-box')
    page_data = page_box.get("page-data")
    totalPage = eval(page_data).get("totalPage")
    # page_box.get("page-url")

    for i in range(1, 1 + int(totalPage)):
        if i != 1:
            newPageUrl = url + "pg{}".format(i)
            html = reqPage(newPageUrl)
            soup = BeautifulSoup(html, "lxml")

        rs = soup.find_all("div", attrs={"class": "info clear"})

        print(len(rs))
        for unit in rs:
            baseInfo = unit.find('div', attrs={'class': 'houseInfo'})
            positionInfo = unit.find('div', attrs={'class': 'positionInfo'}).find('a', attrs={'data-el': 'region'})
            priceinfo = unit.find('div', attrs={'class': 'totalPrice'})

            # positionInfo = position.find('a', attrs={'data-el': 'region'})
            # print(positionInfo.get("href"), positionInfo.get_text())

            position = positionInfo.get_text()
            price = priceinfo.find("span").get_text()
            baseInfo = baseInfo.get_text()

            # arrayHousinfo = []
            arrayHousinfo = villageHouseInfo.get(positionInfo.get("href"))
            if arrayHousinfo is not None:
                arrayHousinfo.append(houseInfo(baseInfo, price, position))
            else:
                villageHouseInfo[positionInfo.get("href")] = [houseInfo(baseInfo, price, position)]

        time.sleep(4)

    return area_total, __average__(villageHouseInfo)


def __average__(villageHouseInfo):
    allVilageAverage = 0
    for (k, v) in villageHouseInfo.items():
        print(v[0].getVillageName())
        villageTotalAverage = 0

        print(v[0].getVillageName(), k)
        for item in v:
            villageTotalAverage += item.getAveragePrice()
        allVilageAverage += villageTotalAverage / len(v)
        print("village average:", villageTotalAverage / len(v), "yuan/pingmi")

    return villageTotalAverage / len(villageHouseInfo)


def testAveragePrice():
    str = "2室1厅 | 71.56平米 | 南 | 简装 | 高楼层(共6层) | 1995年建 | 板楼"

    hi = houseInfo(str, "110", "")
    print(hi.getAveragePrice())


if __name__ == '__main__':
    testAveragePrice()

    totalNum, mp = update("/ershoufang/datuanzhen/")
    if totalNum is not None:
        print(totalNum)
        for (k, v) in mp.items():
            print(v[0].getVillageName())
            villageTotalAverage = 0
            for item in v:
                villageTotalAverage += item.getAveragePrice()

            print("average:", villageTotalAverage / len(v), "yuan/pingmi")
