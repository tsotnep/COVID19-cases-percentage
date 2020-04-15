# -*- coding: utf-8 -*-
import scrapy


class ParseCasesSpider(scrapy.Spider):
    name = 'parse_cases'
    allowed_domains = ['https://www.worldometers.info/coronavirus/']
    start_urls = ['https://www.worldometers.info/coronavirus/']

    def parse(self, response):
        for row in response.xpath('//*[@id="main_table_countries_today"]'):
            for i in range(9, 220):
                yield{ 
                    'country'   :             row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[1]/a/text()').extract_first(),
                    'cases'     : int('0'+''.join(row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[2]/text()').re(r"(\d+)"))),
                    'deaths'    : int('0'+''.join(row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[4]/text()').re(r"(\d+)"))),
                    'recovered' : int('0'+''.join(row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[6]/text()').re(r"(\d+)"))),
                    'active'    : int('0'+''.join(row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[7]/text()').re(r"(\d+)"))),
                    'tests'     : int('0'+''.join(row.xpath('//*[@id="main_table_countries_today"]/tbody[1]/tr['+str(i)+']/td[11]/text()').re(r"(\d+)")))
                }               
