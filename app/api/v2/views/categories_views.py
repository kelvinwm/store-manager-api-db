from flask_restful import Resource
from app.api.v2.models.categories_model import Categories


class CategoriesModel(Resource):
    """Create categories and read them"""

    def __init__(self):
        self.category = Categories()

    def post(self):
        """Add a category"""
        return self.category.add_category()

    def get(self):
        """get all categories"""
        return self.category.get_all_categories()


class SingleCategory(Resource):
    """Modify and delete a category"""

    def __init__(self):
        self.category = Categories()

    def put(self, category_id):
        """Update category by id"""
        return self.category.update_category(category_id)

    def delete(self, category_id):
        """delete category"""
        return self.category.delete_category(category_id)