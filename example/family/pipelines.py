from scrapy_toolbox.database import DatabasePipeline
import family.items as items
import family.models as models

class FamilyPipeline(DatabasePipeline):
    def __init__(self, settings):
        super().__init__(settings, items, models)
