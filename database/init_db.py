from database.connection import engine
from database.model import Base

Base.metadata.create_all(bind=engine)
print("Database tables created.")
