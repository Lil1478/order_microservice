from database import Base, engine
from models.order_model import User

print("Create database...")
Base.metadata.create_all(engine)