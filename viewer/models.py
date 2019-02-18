# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from mongoengine import *


@python_2_unicode_compatible
class JobField(Document):
    # 职位ID
    job_id = StringField('ID')
    # 职位名称
    job_name = StringField(max_length=256)
    # 职位城市
    job_city = StringField(max_length=256)
    # 抓取地区
    area = StringField(max_length=256)
    # 抓取关键词
    key_word = StringField(max_length=256)
    # 职位创建时间
    create_time = DateTimeField()
    # 工资(未处理前, 为字符串形式)
    salary = StringField(max_length=50)
    # 最低工资
    salary_min = FloatField()
    # 最高工资
    salary_max = FloatField()
    # 平均工资
    salary_avg = FloatField()
    # 公司
    company = StringField(max_length=256)

    # 指定数据表格
    meta = {'collection': 'jobinfo'}

    def __str__(self):
        pass


class RankField(Document):
    name = StringField()
    month = IntField()
    ranking = StringField()
    ratio = StringField()

    meta = {'collection': 'tiobe'}

