"""Seed database with sample data from CSV Files."""
from csv import DictReader
from app import db
from models import db, connect_db, User, TajweedRules, UserTajweedStats

db.drop_all()
db.create_all()

with open('generator/rules.csv') as rules:
    db.session.bulk_insert_mappings(TajweedRules, DictReader(rules))


db.session.commit()