import scrapy
from scrapy_splash import SplashRequest
from scrapy.selector import Selector
class UsProxySpider(scrapy.Spider):
    #name of the spider for crawling
    name = 'usproxy'

    #requesting url to crawl
    def start_requests(self):
        url = 'https://us-proxy.org'
        yield SplashRequest(url=url, callback=self.parse,endpoint = 'render.html',args={'wait' : 0.5})
        yield SplashRequest(url=url, callback=self.parse_other_pages,endpoint = 'execute',args={'wait' : 0.5, 'lua_source' : self.script},dont_filter=True)

    #response
    def parse(self, response):
        for data in response.selector.xpath("//table[@id='proxylisttable']/tbody/tr"):
            yield{
                'ip' : data.xpath(".//td[1]/text()").extract_first(),
                'port' : data.xpath(".//td[2]/text()").extract_first()
            }

    def parse_other_pages(self, response):
        for page in response.data:
            sel = Selector(text=page)
            for data in sel.xpath("//table[@id='proxylisttable']/tbody/tr"):
                yield{
                    'ip' : data.xpath(".//td[1]/text()").extract_first(),
                    'port' : data.xpath(".//td[2]/text()").extract_first()
                }