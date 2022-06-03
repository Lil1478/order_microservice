import configparser

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


print("Init database...")

config = configparser.ConfigParser()
config.read("configuration.ini")

postgres_config = config["postgresql"]

# #local
db_host = postgres_config["host"]
db_port = postgres_config["port"]
db_user = postgres_config["user"]
db_pass = postgres_config["passwd"]
db_name = postgres_config["db"]


db_url = (
    "postgresql://"
    + db_user
    + ":"
    + db_pass
    + "@"
    + db_host
    + ":"
    + db_port
    + "/"
    + db_name
)

print(db_url)

engine = create_engine(db_url)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine)
