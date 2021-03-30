from inspect import getmembers, isclass
# Get all classes from a *.py-script
from sqlalchemy.inspection import inspect
# Get PKs from model-class

class ItemsModelMapper:

    # For each Item there has to be a corrisponding databaseobject that extends scrapy_toolbox.database.DeclarativeBase
    # The naming must be XYItem for Item and XY for databaseobject
    # The item must have a ids variable with all the names of primary-keys to filter or empty list

    def __init__(self, items, model):
        self.items = items
        self.model = model
        self.model_col = {cls_name + "Item" : cls_obj for cls_name, cls_obj in
                          getmembers(self.model) if isclass(cls_obj)}  # "XYItem" : XY.__class_


    def map_to_model(self, item, sess):
        item_class = item.__class__
        item_fields = list(item.keys())
        model_class = self.model_col[item_class.__name__]
        ids = [key.name for key in inspect(model_class).primary_key]
        if not self.check_ids(item_fields, ids):
            item = model_class(**{i:item[i] for i in item})
            return item
        filter_param = {item_id:item[item_id] for item_id in ids}
        item_by_id = sess.query(model_class).filter_by(**filter_param).first()
        if item_by_id is None:
            item = model_class(**{i:item[i] for i in item})
        else:
            item = item_by_id
        return item

    def check_ids(self, item_fields, ids):
        contains = True
        for obj_id in ids:
            contains = contains and (obj_id in item_fields)
        return contains