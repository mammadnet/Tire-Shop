from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# The Engine is the starting point for any SQLAlchemy application. 
# It's configured here to connect to a local SQLite database file.
engine = create_engine("sqlite:///database/database.db")

# A sessionmaker object is a factory for creating new Session objects.
# It's bound to our engine, so any session created will use this database connection.
Session = sessionmaker(bind=engine)

# To interact with the database, we instantiate the Session class.
# This 'session' object is the primary interface for all database operations.
session = Session()

# This Base class will be used as the parent for all of our ORM models.
# Any class that inherits from Base will be mapped to a table in the database.
Base = declarative_base()