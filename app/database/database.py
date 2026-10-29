
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.engine import make_url

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "mysql+pymysql://root:@localhost/ai_api_analyzer"
)

# Normalize the MySQL driver
if DATABASE_URL.startswith("mysql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "mysql://", "mysql+pymysql://", 1
    )
elif DATABASE_URL.startswith("mysql+mysqldb://"):
    DATABASE_URL = DATABASE_URL.replace(
        "mysql+mysqldb://", "mysql+pymysql://", 1
    )

# Remove URL parameters that PyMySQL cannot use as connection arguments
url = make_url(DATABASE_URL)
query = dict(url.query)

ssl_mode = query.pop("ssl-mode", None)
query.pop("ssl_mode", None)

url = url.set(query=query)

connect_args = {}

# Enable TLS for the Aiven database
if os.getenv("DATABASE_URL") and ssl_mode:
    connect_args["ssl"] = {}

engine = create_engine(
    url,
    pool_pre_ping=True,
    future=True,
    connect_args=connect_args
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
