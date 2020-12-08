import scrapy
from scrapy.http import TextResponse
from bs4 import BeautifulSoup

class TheidiomsComSpider(scrapy.Spider):
    name = "theidioms_com"
    allowed_domains = ["theidioms.com"]
    start_urls = ["http://theidioms.com/list/"]

    def parse(self, response: TextResponse):
        for link in response.selector.css("a.rm"):
            yield response.follow(link, callback=self.parse_detail_view)
        next_page = response.selector.css("span.next>a::attr(href)").get()
        yield scrapy.Request(url=next_page)

    def parse_detail_view(self, response: TextResponse):
        idiom = response.css("#phrase strong::text").get()
        example_nodes = response.xpath('//ol[@type="1"]//li')
        for node in example_nodes:
            example = "".join(node.xpath('./descendant-or-self::*/text()').getall())
            yield {"idiom": idiom, "example": example}
