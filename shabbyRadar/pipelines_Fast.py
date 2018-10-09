# -*- coding: utf-8 -*-
class ShabbyradarPipeline(object):

    def process_item(self, item, spider):
        if "--" not in item['value1'] and "--" not in item['value2']:
            spider.dataRepository.append([item['date'],
                                          item['id'],
                                          item['name'],
                                          item['value1'],
                                          item['value2'].replace("%", "")])

        if len(spider.dataRepository) >= 5000:
            spider.insert_by_many()

        return item