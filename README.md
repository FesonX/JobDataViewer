# JobDataViewer

Scroll down to get English version.

# 基于Django的数据可视化项目

## 开发环境：

1. Python 3.6

2. Django 1.11.8

3. 数据可视化插件：Highcharts

4. 数据库：MongoDB

   

## 数据源

数据源来自51Job

使用Scrapy抓取

爬取项目源代码，请移步 [[JobCrawler](https://github.com/FesonX/JobCrawler)](https://github.com/FesonX/JobCrawler) 



## 运行

运行需要Python3，MongoDB，请先安装

然后在键入`pip install -r requirements.txt`安装Python库文件

最后键入`python manage.py runserver`



## 停止

使用Ctrl + C终止服务器运行


## 运行截图
* 平均工资
![01](/TestImages/01.png)

* 工资走向
![02](/TestImages/02.png)

* 职位数量 Top25
![03](/TestImages/03.png)

* 城市职位数量比例
![04](/TestImages/04.png)

* 平均工资表
![05](/TestImages/05.png)



# A Django Project For Data in JobCrawler Visualization.

### Developing Environment:

1. Python Ver: 3.6
2. Django 1.11.8
3. Data Visualization Tool: Highcharts
4. Database: MongoDB

## Data
Data From 51Job
Use Scrapy to crawl data.
You can find the project in [JobCrawler](https://github.com/FesonX/JobCrawler)

## Run JobDataViewer
Before Running the project, type`pip install -r requirements.txt` to install requirements.

type `python manage.py runserver` in terminal

## Stop JobDataViewer
use Ctrl + C to stop server.

## Running Demo ScreenShots
* Average Salary
![01](/TestImages/01.png)

* Salary Trend
![02](/TestImages/02.png)

* Post Counts Top25
![03](/TestImages/03.png)

* City Ratio of Job Counts
![04](/TestImages/04.png)

* Average Salary Table
![05](/TestImages/05.png)

## Version Update

## Ver1.1 5/24,2018
### Ajax Support Available
Now Salary Trend Function developed with Ajax, bringing higher speed than ver 1.0
Before using ajax, open the page cost 1min 30s, comparing 18s-20s now.
Special thanks to [@huangjiarong](https://github.com/huangjiarong)