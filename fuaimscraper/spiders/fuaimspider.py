import scrapy
from fuaimscraper.items import FuaimItem


class FuaimspiderSpider(scrapy.Spider):
    name = "fuaimspider"
    allowed_domains = ["fuaimeanna.ie"]
    start_urls = ["http://fuaimeanna.ie/en/Recordings.aspx?Page=1"]

    def parse(self, response):
        pronunciations = response.css('div.friotal')

        for pronunciation in pronunciations:

            fuaim_item = FuaimItem()

            fuaim_item['ortho'] = pronunciation.css('span.ortho::text').get(),
            fuaim_item['translation'] = pronunciation.css(
                'span.translation::text').get(),
            fuaim_item['url'] = pronunciation.css(
                'span.taifead source').attrib['src'],

            yield fuaim_item

        next_page = response.css('div.pager a.right ::attr(href)').get()

        if next_page is not None:
            next_page_url = "http://fuaimeanna.ie/en/Recordings.aspx" + next_page
            yield response.follow(next_page_url, callback=self.parse)
