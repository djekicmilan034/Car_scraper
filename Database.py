import psycopg2
import sqlalchemy
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *

engine=create_engine('postgresql://postgres:root@localhost:5432/advertisment',echo=False) #Konekcija sa bazom.
Session=sessionmaker(bind=engine)
session=Session()
Base=sqlalchemy.orm.declarative_base()

class Oglas(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True,autoincrement=True)
    title = Column(String)
    location = Column(String)
    price = Column(Integer)
    posted = Column(Date)
    link = Column(String)
    fuel = Column(String)
    type = Column(String)
    cm3 = Column(Integer)
    km = Column(Integer)
    year = Column(Integer)
    kw = Column(Integer)
    horse_power=Column(Integer)

def add_oglas(title, location, price, posted, link, fuel, type, cm3, km, year, kw,horse_power):
    session = Session()
    oglas = Oglas(title=title, location=location, price=price, posted=posted, link=link, fuel=fuel, type=type, cm3=cm3, km=km,year=year, kw=kw, horse_power=horse_power)
    session.add(oglas)
    session.commit()

#Provera da li postoji konekcija sa bazom demo, sto znaci da je pre pokretanja programa potrebno napraviti bazu u pgAdmin-u.
try:
    connection = psycopg2.connect(user="postgres", password="root", host="localhost", port="5432", database="advertisment")
    print("Connection established")
except (Exception, psycopg2.Error) as error:
    print("Connection not established", error)

#Provera da li postoji tabela 'ads' u bazi demo.
cursor = connection.cursor()
cursor.execute(f"SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_name='ads')")
if bool(cursor.fetchone()[0]):
    print(f'Table ads exists.')
#Ukoliko ne postoji tabela 'neks' u bazi, program ce je kreirati.
else:
    print(f'Table ads does not exist. Creating the Table ads now.')
    Base.metadata.create_all(engine)
    session.commit()