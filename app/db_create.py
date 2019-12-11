from config import SQL_ALCHEMY_DATABASE_URI
from . import db
import os.path

db.create_all()