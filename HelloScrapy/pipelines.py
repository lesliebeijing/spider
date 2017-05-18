# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql


class HelloscrapyPipeline(object):
    def process_item(self, item, spider):
        return item


class CompanyPipeline(object):
    def open_spider(self, spider):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='',
                                          db='mydb', charset='utf8')

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        try:
            with self.connection.cursor() as cursor:
                sql = "SELECT * FROM `company` WHERE `name`=%s"
                cursor.execute(sql, (item.get('name'),))
                result = cursor.fetchone()

                if not result:
                    # Create a new record
                    sql = "INSERT INTO `company` (`name`, `region`,`nature`,`size`,`web_site`,`address`,`introduction`) VALUES (%s, %s,%s,%s,%s,%s,%s)"
                    cursor.execute(sql, (item.get('name'), item.get('region', ''), item.get('nature', '')
                                         , item.get('size', ''), item.get('web_site', ''), item.get('address', ''),
                                         item.get('introduction', '')))

                    self.connection.commit()
        except Exception as e:
            logging.error(e)

        return item
