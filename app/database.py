from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# set up API DB params
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# connect request to a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', 
#                                 database='FAST_API', 
#                                 user='postgres',
#                                 password='postgres',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Seccessfully connected to the DB')

#         break
#     except Exception as err:
#         print(f'Connection to the database failed due to {err}')
#         time.sleep(5)