import os


class cvs:
    def __init__(self,listInfo):
        self.list = listInfo

    def start(self,filename, ):
        print(os.getcwd())  # 获得当前目录
        csv_file = os.getcwd() + "/{0}.csv".format(filename)
        with open(csv_file, "w") as f:
            # 开始获得需要的板块数据
            ershous = self.get_area_ershou_info(city_name, area_name)
            # 锁定，多线程读写
            if self.mutex.acquire(1):
                self.total_num += len(ershous)
                # 释放
                self.mutex.release()
            if fmt == "csv":
                for ershou in ershous:
                    # print(date_string + "," + xiaoqu.text())
                    f.write(self.date_string + "," + ershou.text() + "\n")
        print("Finish crawl area: " + area_name + ", save data to : " + csv_file)
