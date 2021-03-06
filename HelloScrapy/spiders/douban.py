import re

import scrapy

"""
豆瓣搜索图书并爬取列表信息
"""


class DoubanSpider(scrapy.Spider):
    name = "douban"
    search_keys = ['数据挖掘', '数据分析', '数据科学', 'python数据分析']
    page_size = 15

    def start_requests(self):
        for key in self.search_keys:
            for i in range(0, 100):
                start = i * self.page_size
                url = 'https://book.douban.com/subject_search?start=%s&search_text=%s&cat=1001' % (start, key)
                yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        lis = response.xpath('//li[@class="subject-item"]')

        for li in lis:
            score = li.xpath('div[@class="info"]/div[2]/span[2]/text()').extract_first()
            if score and float(score) >= 7.0:
                img_url = li.xpath('div[@class="pic"]/a/img/@src').extract_first()
                comments = li.xpath('div[@class="info"]/div[2]/span[3]/text()').extract_first()
                title = li.xpath('div[@class="info"]/h2/a/@title').extract_first()
                url = li.xpath('div[@class="info"]/h2/a/@href').extract_first()
                pub = li.xpath('div[@class="info"]/div[@class="pub"]/text()').extract_first()
                press = ''
                press_year = ''
                author = ''
                if pub:
                    pub = pub.strip()
                    press_arr = re.split(r'\s+/\s+', pub)
                    if len(press_arr) == 4:
                        author = press_arr[0]
                        press = press_arr[1]
                        press_year = press_arr[2]
                    elif len(press_arr) == 5:
                        author = ' / '.join(press_arr[0:2])
                        press = press_arr[2]
                        press_year = press_arr[3]

                # if press_year:
                #     tmp = re.split(r'-', press_year)
                #     year = int(tmp[0])
                #     cur_year = time.localtime(time.time()).tm_year
                #     if cur_year - year > 10:
                #         # 只看 10 年以内的
                #         continue

                comments_count = 0
                if comments:
                    comments = comments.strip()
                    cnt = re.findall(r'\d+', comments)
                    if cnt:
                        comments_count = int(cnt[0])

                print(title, img_url, author, press, press_year, score, comments_count)

                yield {
                    'name': title,
                    'img_url': img_url,
                    'url': url,
                    'author': author,
                    'press': press,
                    'press_year': press_year,
                    'score': float(score),
                    'comments_count': comments_count
                }
