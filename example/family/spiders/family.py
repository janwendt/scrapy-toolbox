from scrapy_toolbox.error_handling import ErrorCatcher
import scrapy
from scrapy.loader import ItemLoader
from family.items import MotherItem, ChildItem
import family.models as models

class FamilySpider(scrapy.Spider, metaclass=ErrorCatcher):
    name = "family"

    start_urls = ["https://github.com/janwendt/scrapy-toolbox"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url)

    def parse(self, response):
        # Add Mother
        mother = ItemLoader(item=MotherItem(), response=response)
        mother.add_value('name', 'Jane Doe')
        yield mother.load_item()

        # Add Child
        child = ItemLoader(item=ChildItem(), response=response)
        child.add_value('mother_id', mother.item["id"])
        child.add_value('name', 'John Doe')
        yield child.load_item()

        # Query all Mothers from Database and print their name and children model objects
        session = self.crawler.database_session
        for m in session.query(models.Mother).all():
            print(m.name)
            print(m.children)
