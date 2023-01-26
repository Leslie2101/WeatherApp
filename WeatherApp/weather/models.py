from . import db
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cityname = db.Column(db.String(50))




        


