import scrapy
import os
import re


class TaoBaoSpider(scrapy.Spider):
    name = "taobao"

    def start_requests(self):
        file = open(os.path.join(os.path.abspath('.'), 'taobao.txt'))
        i = 1
        while True:
            # if i > 100:
            #     break

            url = file.readline().strip()

            if not url:
                break

            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

            i += 1

        print('total count:', i)

    def parse(self, response):
        url = response.request.url
        if 'taobao' in url:
            name = response.xpath('//div[@id="J_Title"]/h3/text()').extract_first()
            if name:
                name = name.strip()

            if not name:
                name = response.xpath('//div[@id="J_Title"]/h3/@data-title').extract_first()
                if name:
                    name = name.strip()

            brand = response.xpath('//div[@id="attributes"]/*').re(
                r'<li title="(.+?)">.*?(品牌)[:：](.+?)</li>')
            if brand and len(brand) == 3:
                brand = brand[0].strip()
            else:
                brand = ''

            price = response.xpath('//*[@id="J_StrPrice"]/em[@class="tb-rmb-num"]/text()').extract_first()

            guige = response.xpath('//div[@id="attributes"]//text()').re(r'.*?(净含量|型号|规格)[:：](.*)')
            if guige and len(guige) >= 2:
                guige = guige[1].strip()
            else:
                guige = ''

            tongyongming = response.xpath('//div[@id="attributes"]/*').re(
                r'<li title="(.+?)">.*?(产品名称|通用名)[:：](.+?)</li>')
            if tongyongming and len(tongyongming) == 3:
                tongyongming = tongyongming[0].strip()
            else:
                tongyongming = ''
        else:
            name = response.xpath('//h1[@data-spm]/text()').extract_first()
            if name:
                name = name.strip()

            if not name:
                name = response.xpath('//h1[@data-spm]/a/text()').extract_first()
                if name:
                    name = name.strip()

            brand = response.xpath('//li[@id="J_attrBrandName"]/@title').extract_first()
            if brand:
                brand = brand.strip()

            price = response.xpath('//text()').re_first(r'"defaultItemPrice":"(.+?)"')

            guige = response.xpath('//div[@id="J_AttrList"]//text()').re(r'.*?(净含量|型号|规格)[:：](.*)')
            if guige and len(guige) >= 2:
                guige = guige[1].strip()
            else:
                guige = ''

            tongyongming = response.xpath('//*[@id="J_AttrUL"]/li[9]/@title').extract_first()
            if tongyongming:
                tongyongming = tongyongming.strip()

        # columns = ['品牌', '品名', '通用名', '规格', '参考价', '链接']

        data = {
            'brand': brand,
            'name': name,
            'tongyongming': tongyongming,
            'guige': guige,
            'price': price,
            'url': url,
        }
        print(data)
        yield data
