# JobDataViewer

# A Django Project For Data in JobCrawler Visualization.
Developing Environment:
1. Python Ver: 3.6
2. Django 1.11.8
3. Data Visualization Tool: Highcharts
4. Database: MongoDB

## Data
Data From 51Job
Use Scrapy to crawl data.
You can find the project in [JobCrawler](https://github.com/FesonX/JobCrawler)

## Run JobDataViewer
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