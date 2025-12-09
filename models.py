from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Float, Text, Column
import json

db = SQLAlchemy()

class Recipe(db.Model):
    __tablename__ = 'recipes'
    id = Column(Integer, primary_key=True)
    cuisine = Column(String(255), nullable=True)
    title = Column(String(1024), nullable=False)
    rating = Column(Float, nullable=True)
    prep_time = Column(Integer, nullable=True)
    cook_time = Column(Integer, nullable=True)
    total_time = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    nutrients = Column(Text, nullable=True)  # store JSON as text for SQLite
    serves = Column(String(255), nullable=True)
    calories = Column(Integer, nullable=True)  # derived numeric calories for filtering

    def to_dict(self):
        nutrients_obj = None
        try:
            if self.nutrients:
                nutrients_obj = json.loads(self.nutrients)
        except Exception:
            nutrients_obj = None
        return {
            "id": self.id,
            "title": self.title,
            "cuisine": self.cuisine,
            "rating": self.rating,
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "total_time": self.total_time,
            "description": self.description,
            "nutrients": nutrients_obj,
            "serves": self.serves
        }
