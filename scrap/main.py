import json
import scrapy
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerProcess
from scrapy.item import Item, Field

class QuoteItem(Item):
    quote = Field()
    author = Field()
    tags = Field()

class AuthorItem(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()

class DataPipeline:
    quotes = []
    authors = []

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if 'fullname' in adapter.keys():
            self.authors.append(dict(adapter))
        if 'quote' in adapter.keys():
            self.quotes.append(dict(adapter))
        return item

    def close_spider(self, spider):
        with open('json_files/quotes.json', 'w', encoding='utf-8') as fh:
            json.dump(self.quotes, fh, ensure_ascii=False, indent=2)
        with open('json_files/authors.json', 'w', encoding='utf-8') as fh:
            json.dump(self.authors, fh, ensure_ascii=False, indent=2)

class QuotesSpider(scrapy.Spider):
    name = "get_quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["http://quotes.toscrape.com/"]
    custom_settings = {
        "ITEM_PIPELINES": {
            '__main__.DataPipeline': 300,
        }
    }

    def parse(self, response):
        for q in response.xpath("//div[@class='quote']"):
            quote = q.xpath("span[@class='text']/text()").get().strip()
            author = q.xpath("span/small[@class='author']/text()").get().strip()
            tags = q.xpath("div[@class='tags']/a/text()").extract()
            yield QuoteItem(quote=quote, author=author, tags=tags)

            author_url = q.xpath("span/a[contains(@href, 'author')]/@href").get()
            if author_url:
                yield response.follow(url=author_url, callback=self.parse_author)

        next_link = response.xpath("//nav//li[@class='next']/a/@href").get()
        if next_link:
            yield response.follow(url=next_link, callback=self.parse)

    def parse_author(self, response):
        fullname = response.xpath("//h3[@class='author-title']/text()").get().strip()
        born_date = response.xpath("//span[@class='author-born-date']/text()").get().strip()
        born_location = response.xpath("//span[@class='author-born-location']/text()").get().strip()
        description = response.xpath("//div[@class='author-description']/text()").get().strip()
        yield AuthorItem(fullname=fullname, born_date=born_date, born_location=born_location, description=description)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(QuotesSpider)
    process.start()
