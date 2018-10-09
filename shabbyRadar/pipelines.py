# -*- coding: utf-8 -*-
class ShabbyradarPipeline(object):

    def process_item(self, item, spider):
        # 使用cursor()方法获取操作游标
        cursor = spider.db.cursor()

        if "--" not in item['value1'] and "--" not in item['value2']:
            # SQL 插入语句
            sql = "INSERT INTO MonetaryFund \
                   VALUES ('%s', '%s', '%s', '%s', '%s')" % \
                  (item['date'],
                   item['id'],
                   item['name'],
                   item['value1'],
                   item['value2'].replace("%", ""),
                   )
            # try:
                # 执行sql语句
            cursor.execute(sql)
                # 提交到数据库执行
            spider.db.commit()
            # except:
            #     # 如果发生错误则回滚
            #     spider.db.rollback()
        return item
