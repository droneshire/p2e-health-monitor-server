"""
Server config
"""
from os import path

basedir = path.abspath(path.dirname(__file__))

# Database connection variables
SQLALCHEMY_DATABASE_URI = "sqlite:///" + path.join(basedir, "database", "p2e_health.db")
