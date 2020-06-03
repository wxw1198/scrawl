#!/bin/bash
HOSTNAME="127.0.0.1"                                           #数据库信息
PORT="3306"
USERNAME="root"
PASSWORD="123"
DBNAME="houseDB"                                                 #数据库名称
#TABLENAME="spyUserTable"                                         #数据库中表的名称
 
#创建数据库
create_db_sql="create database IF NOT EXISTS ${DBNAME} CHARACTER SET 'utf8' COLLATE 'utf8_general_ci'"
mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} -e "${create_db_sql}"
 
 
TABLENAME="cities"                                         #数据库中表的名称
#create program table
create_table_program="create table IF NOT EXISTS ${TABLENAME} (
timeNow varchar(32),  
url varchar(512), 
cityName varchar(64) DEFAULT '',  #城市名称
averagePrice int,  #房产均价
count int(128),
primary key (timeNow,url)) " #房产总数

mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} ${DBNAME} -e "${create_table_program}"

TABLENAME="countyTowns"                                         #区、县数据表
#create program table
create_table_program="create table IF NOT EXISTS ${TABLENAME} (  
timeNow varchar(32),
url varchar(512), 
countyTownname  varchar(64) DEFAULT '',  #城市名称
averagePrice int,  #房产均价
totalNumber int(128),
primary key (timeNow,url)) " #房产总数

mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} ${DBNAME} -e "${create_table_program}"

TABLENAME="districts"                                         #街区、乡镇
#create program table
create_table_program="create table IF NOT EXISTS ${TABLENAME} ( 
timeNow varchar(32), 
url varchar(512), 
districtName  varchar(64) DEFAULT '',  #城市名称
averagePrice int,  #房产均价
count int(128),
primary key (timeNow,url)) " #房产总数

mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} ${DBNAME} -e "${create_table_program}"


TABLENAME="villages"                                         #小区
#create program table
create_table_program="create table IF NOT EXISTS ${TABLENAME} (  
timeNow varchar(32),
url varchar(512), 
villageName  varchar(64) DEFAULT '',  #城市名称
averagePrice int,  #房产均价
count int(128),
primary key (timeNow,url)) " #房产总数

mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} ${DBNAME} -e "${create_table_program}"



TABLENAME="houseInfo"                                         #小区
#create program table
create_table_program="create table IF NOT EXISTS ${TABLENAME} ( 
timeNow varchar(32), 
url varchar(512), 
baseInfo  varchar(128) DEFAULT '',  #城市名称
positionInfo varchar(32),  #房产均价
priceInfo  varchar(32),
primary key (timeNow,url)) " #房产总数

mysql -h${HOSTNAME}  -P${PORT}  -u${USERNAME} -p${PASSWORD} ${DBNAME} -e "${create_table_program}"
