import scrapy

from ..items import CompanyItem


class ZhilianSpider(scrapy.Spider):
    name = "zhilian"
    search_keys = ['android', 'ios', 'java', '.net', 'c', 'c++', 'php', 'unity', 'unreal', 'linux', 'python',
                   '测试', '嵌入式', '前端', '大数据', '运维', '机器学习']

    def start_requests(self):
        for key in self.search_keys:
            url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?jl=青岛&kw=%s&p=1&isadv=0' % key
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        companies = response.css('table.newlist')
        for company in companies:
            name = company.css('td.gsmc a::text').extract_first()
            region = company.css('td.gzdd::text').extract_first()

            detail_url = company.css('td.gsmc a::attr(href)').extract_first()
            if detail_url and 'special.zhaopin.com' not in detail_url:
                yield scrapy.Request(detail_url, callback=self.parse_detail, meta={'name': name, 'region': region})

        next_page = response.xpath('//li[@class="pagesDown-pos"]/a/@href').extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_detail(self, response):
        name = response.meta.get('name')
        region = response.meta.get('region')
        table_desc = response.css('table.comTinyDes')
        items = table_desc.css('tr td span')
        nature = ''
        size = ''
        address = ''
        web_site = ''

        if len(items) == 8:
            nature = items[1].css('::text').extract_first()  # 性质
            size = items[3].css('::text').extract_first()  # 公司规模
            address = items[7].css('::text').extract_first()  # 地址
        elif len(items) == 10:
            nature = items[1].css('::text').extract_first()  # 性质
            size = items[3].css('::text').extract_first()  # 公司规模
            web_site = items[5].css('a::attr(href)').extract_first()  # 网站
            address = items[9].css('::text').extract_first()  # 地址

        if web_site and web_site == 'http://null':
            web_site = ''

        introduction = ''
        intros = response.xpath('//div[@class="company-content"]//*').extract()  # 简介
        for intro in intros:
            introduction += intro.strip()

        company_item = CompanyItem({
            'name': name,
            'region': region,
            'nature': nature,
            'size': size,
            'web_site': web_site,
            'address': address,
            'introduction': introduction
        })

        yield company_item
