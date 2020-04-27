# -*- coding: utf-8 -*-
import scrapy


class ParsePopulationSpider(scrapy.Spider):
    name = 'parse_population'
    allowed_domains = ['https://www.worldometers.info/world-population/population-by-country/']
    start_urls = ['https://www.worldometers.info/world-population/population-by-country/']

    def parse(self, response):
        for row in response.xpath('//*[@id="example2"]'):
            for i in range(1, 236):
                yield{ 
                    'country'   : row.xpath('//*[@id="example2"]/tbody/tr['+str(i)+']/td[2]/a/text()').extract_first(),
                    'population': int('0'+''.join(row.xpath('//*[@id="example2"]/tbody/tr['+str(i)+']/td[3]/text()').re(r"(\d+)"))), #remove ',' and to_int, write 0 if not available
                    'medAge'    : int('0'+''.join(row.xpath('//*[@id="example2"]/tbody/tr['+str(i)+']/td[10]/text()').re(r"(\d+)")))
                }