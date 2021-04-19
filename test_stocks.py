import sqlite3
from datetime import datetime

import sqlalchemy.exc
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Boolean,
    create_engine,
    DateTime,
    func,
    ForeignKey,
)
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, session
import csv, pathlib, os

# users_table = Table(
#     'users',
#     metadata,
#     Column('id',Integer,primary_key=True),
#     Column('username',String(30),unique=True),
#     Column('is_staff',Boolean,nullable=False,default=False), # oly 1 or 0
# )s
def get_companies_names_price_earnings():
    '''
    :return:
    '''
    file = os.path.join(os.getcwd(), 's-and-p-500-companies-financials', 'data', 'constituents-financials.csv')
    companies_ticker = []
    companies_name = []
    price_earnings = []
    mark_cap = []
    print('file path:', file)
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            # print(', '.join(row))
            companies_ticker.append(row[0])
            companies_name.append(row[1])
            price_earnings.append(row[3])
            mark_cap.append(row[10])
    return (companies_name,companies_ticker,price_earnings,mark_cap)


engine = create_engine('sqlite:///stocks.db', echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Stock(Base):
    __tablename__ = 'stock_info'
    def __init__(self,
                 stock_name:str,
                 stock_ticker:str,
                 stockable:bool = True,
                 mark_cap:int = 0.0):

        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        self.stockable = stockable #this year
        self.mark_cap = mark_cap #this eyar

    id = Column(Integer,primary_key=True) #id
    stock_name = Column(String(40),nullable=False,default='',server_default='')
    stock_ticker = Column(String(40),nullable=False,default='',server_default='')
    stockable = Column(Boolean, nullable=False, default=True, server_default= '1')
    mark_cap = Column(Integer, nullable=False, default=0, server_default='0')
    record_date = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    def __str__(self):
        return f"current stock info: (id = {self.id}," \
               f"name={self.stock_name!r}," \
               f"ticker={self.stock_ticker!r}," \
               f"cap={self.mark_cap!r} )" \
               f"if sotockable?={self.stockable!r} )"


    def __repr__(self):
        return str(self)

def write_stock(stock):
    session = Session()
    for c in stock:
        print(c)
    stock_filling = Stock(
        stock_name=(stock[0]),
        stock_ticker=(stock[1]),
        stockable=True,
        mark_cap=stock[3],
    )
    print('printing...',stock_filling)
    session.add(stock_filling)
    session.commit()
    session.close()

def take_one_stock(input,n):
    print('length:',len(input))
    count = 0
    for i in range(len(input)):
        if count == n-1:
            return
        res_list = [stock[count] for stock in input]
        count += 1
        yield res_list # yeield

def take_one_stock_ver0(input):
    res_list = [stock[0] for stock in input]
    return  res_list

if __name__ == '__main__':

    Base.metadata.create_all()
    result = get_companies_names_price_earnings()
    n=5
    stocks = take_one_stock(result,n)
    for i in range(n):
        write_stock( stocks.__next__())
        #write_stock(stock)
    # a_stock = take_one_stock_ver0(result)
    # write_stock(a_stock)

