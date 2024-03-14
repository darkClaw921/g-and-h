from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, JSON, ARRAY, BigInteger, func, text,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from pprint import pprint

load_dotenv()
userName = os.environ.get('POSTGRES_USER')
password = os.environ.get('POSTGRES_PASSWORD')
db = os.environ.get('POSTGRES_DB')
url = os.environ.get('POSTGRES_URL')

print(f'{userName=}')
print(f'{password=}')
print(f'{db=}')

# Создаем подключение к базе данных
engine = create_engine(f'postgresql://{userName}:{password}@{url}:5432/{db}')
# engine = create_engine('mysql://username:password@localhost/games')




 
# Определяем базу данных
Base = declarative_base()


class Contact(Base):
    __tablename__ = 'contact'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    name=Column(String)
    responsible_user_id=Column(Integer)
    # company_id=Column(BigInteger,ForeignKey('Company.id'))
    # leads_id=Column(ARRAY(BigInteger),ForeignKey('Lead.id'))
    # deals_id=Column(ARRAY(BigInteger),ForeignKey('Deal.id'))

class Deal(Base):
    __tablename__ = 'deal'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    status = Column(String)
    close_date = Column(DateTime)
    stage_id = Column(Integer)
    category_id = Column(Integer)
    price=Column(Float)
    products=Column(ARRAY(Float))#(id,price,count)
    assigned_by_id=Column(Integer)
    

class Product(Base):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger)
    created_date = Column(DateTime)
    name=Column(String)
    price=Column(Float)
    category=Column(String)
    deal_id=Column(BigInteger,ForeignKey('deal.id'))


class Company(Base):
    __tablename__ = 'company'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    name=Column(String)
    responsible_user_id=Column(Integer)
    contacts_id=Column(ARRAY(BigInteger))
    leads_id=Column(ARRAY(BigInteger))
    deals_id=Column(ARRAY(BigInteger))


class Lead(Base):
    __tablename__ = 'lead'
    
    id = Column(BigInteger, primary_key=True)
    created_date = Column(DateTime)
    name=Column(String)
    responsible_user_id=Column(Integer)
    status_id=Column(Integer)
    price=Column(Float)
    company_id=Column(BigInteger,ForeignKey('company.id'))
    contacts_id=Column(ARRAY(BigInteger))
    deals_id=Column(ARRAY(BigInteger))
    assigned_by_id=Column(Integer)

class Plan(Base):
    __tablename__ = 'plan'
    
    id = Column(BigInteger, primary_key=True,autoincrement=True)
    start_date = Column(DateTime)
    name=Column(String)
    price=Column(Float)
    type=Column(String)
    user_id=Column(BigInteger,ForeignKey('user.id'))

class User(Base):
    __tablename__ = 'user'
    
    id = Column(BigInteger, primary_key=True)
    # created_date = Column(DateTime)
    name=Column(String)
    last_name=Column(String)
    department=Column(String)

class Department(Base):
    __tablename__ = 'department'
    
    id = Column(BigInteger, primary_key=True)
    name=Column(String)
    parent_id=Column(Integer)
    uf_head=Column(Integer)


Base.metadata.create_all(engine)
# Base.metadata.update()

Session = sessionmaker(bind=engine)
# session = Session()

def add_deal(fields:dict):
    with Session() as session:
        deal = Deal(**fields)
        session.add(deal)
        session.commit()
    return 'ok'

def add_lead(fields:dict):
    with Session() as session:
        lead = Lead(**fields)
        session.add(lead)
        session.commit()
    return 'ok'

def add_product(fields:dict):
    with Session() as session:
        product = Product(**fields)
        session.add(product)
        session.commit()
    return 'ok'

def add_plan(fields:dict):
    with Session() as session:
        plan = Plan(**fields)
        session.add(plan)
        session.commit()
    return 'ok'

def add_department(fields:dict):
    with Session() as session:
        department = Department(**fields)
        session.add(department)
        session.commit()
    return 'ok'



def update_deal(id:int, fields:dict):
    with Session() as session:
        session.query(Deal).filter(Deal.id==id).update(fields)
        session.commit()
    return 'ok'

def update_lead(id:int, fields:dict):
    with Session() as session:
        session.query(Lead).filter(Lead.id==id).update(fields)
        session.commit()
    return 'ok'

def update_product(id:int, fields:dict):
    with Session() as session:
        session.query(Product).filter(Product.id==id).update(fields)
        session.commit()
    return 'ok'


if __name__ ==  '__main__':
    print('start')