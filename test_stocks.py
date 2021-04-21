import sqlite3
from datetime import datetime
from random import randrange
from contextlib import contextmanager
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
from sqlalchemy.orm import sessionmaker, scoped_session, relationship, session, joinedload
import csv, pathlib, os

MAX_STOCKS = 0


def get_companies_names_price_earnings():
    file = os.path.join(os.getcwd(), 's-and-p-500-companies-financials', 'constituents-financials_csv.csv')
    companies_ticker = []
    companies_name = []
    price_earnings = []
    mark_cap = []
    c = 0
    print('file path:', file)
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            # print(', '.join(row))
            c += 1
            companies_ticker.append(row[0])
            companies_name.append(row[1])
            price_earnings.append(row[3])
            mark_cap.append(row[9])
    globals()["MAX_STOCKS"] = c
    return (companies_name, companies_ticker, price_earnings, mark_cap)


engine = create_engine('sqlite:///stocks.db', echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class Stock(Base):
    __tablename__ = 'stock_info'

    def __init__(self,
                 stock_name: str,
                 stock_ticker: str,
                 stockable: bool = True,
                 mark_cap: int = 0.0):
        """
        :param stock_name:
        :param stock_ticker:
        :param stockable:
        :param mark_cap:
        """
        self.stock_name = stock_name
        self.stock_ticker = stock_ticker
        self.stockable = stockable  # this year
        self.mark_cap = mark_cap  # this eyar

    id = Column(Integer, primary_key=True)  # id
    stock_name = Column('Company name', String(40), nullable=False, default='', server_default='')
    stock_ticker = Column('Ticker', String(40), nullable=False, default='', server_default='')
    stockable = Column(Boolean, nullable=False, default=True, server_default='1')
    mark_cap = Column('market capitalization', Integer, nullable=False, default=0, server_default='0')
    record_date = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    def __str__(self):
        return f"current stock info: (id = {self.id}," \
               f"name={self.stock_name!r}," \
               f"ticker={self.stock_ticker!r}," \
               f"cap={self.mark_cap!r} " \
               f"if stockable?={self.stockable!r} )"

    def __repr__(self):
        return str(self)

    financials = relationship("Financials", back_populates="stock0")


class Financials(Base):
    __tablename__ = 'Financials'

    id = Column(Integer, primary_key=True)
    refer_stock_ticker = Column(String, ForeignKey(Stock.stock_ticker), nullable=False)
    year = Column(Integer, nullable=False, unique=True, default='1900', server_default='1900')
    price_earning = Column('Price to earnings', Integer, nullable=False, default='0', server_default='0')
    price_book = Column('Price to book', Integer, nullable=False, default='0', server_default='0')

    def __str__(self):
        return f"stock\'s financials of year:" \
               f"{self.year} are " \
               f"p/e = {self.price_earning}," \
               f"p/b = {self.price_book}"

    def __repr__(self):
        return str(self)

    stock0 = relationship(Stock, back_populates="financials")


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
    print('printing...', stock_filling)
    session.add(stock_filling)
    session.commit()
    session.close()


def take_one_stock(input):
    count = 0
    while True:
        if count == MAX_STOCKS:
            return
        res_list = [stock[count] for stock in input]
        count += 1
        yield res_list  # yeield


def take_one_stock_ver0(input):
    res_list = [stock[0] for stock in input]
    return res_list


def fill_one_financial(ticker: str, year: int = 1900):
    with get_session() as session:
        stock0: Stock = session.query(Stock).filter_by(stock_ticker=ticker).one_or_none()  # asking
        if stock0 is None:
            raise NoSuchStock
        print('current financials:', stock0)
        pe = randrange(1, 100)
        pb = randrange(1, 100)
        fin = Financials(price_book=pb, price_earning=pe, year=year, refer_stock_ticker=stock0.stock_ticker)
        session.add(fin)
    print('financials after', stock0.financials)


class NoSuchStock(Exception):
    """ no such stock"""
    pass


class ParameterIfFIlled(Exception):
    """ this parameter has been already filled"""
    pass


class ErrorDuringSessioning(Exception):
    """ something bad happened"""
    pass

# creating a session manager
@contextmanager
def get_session():
    session0 = Session()
    try:
        yield session0
    #except sqlite3.IntegrityError:
        #print('some error during enquiring to DB')
    except:  # anything else
        session0.rollback()
        raise ErrorDuringSessioning('there is something bad happened')
    else:
        session0.commit()


def get_all_financials(ticker: str):
    with get_session() as session:
        try:
            stock0: Stock = (
                session
                    .query(Stock)
                    .filter_by(stock_ticker=ticker)
                    .options(joinedload(Stock.financials))
                    .one()
            )
        except:  # Error666
            print('There is no such stock')
        else:
            print('stock data = ', stock0)
            print('stock\'s financial:', stock0.financials)

#depricated
def fill_one_financialv2(ticker: str, year: int = 1900):
    stock0: Stock = session.query(Stock).filter_by(stock_ticker=ticker).one_or_none()
    print('current financials:', stock0)
    pe = randrange(1, 100)
    pb = randrange(1, 100)
    try:
        fin = Financials(price_book=pb, price_earning=pe, year=year, refer_stock_ticker=stock0.stock_ticker)
    except sqlite3.IntegrityError:
        session.rollback()
        year += 1
        raise
    else:
        session.add(fin)
        session.commit()
    print('financials after', stock0.financials)
    session.close()


if __name__ == '__main__':
    create_db = 0 # if we starting from blank
    if create_db:  # creating db
        Base.metadata.create_all()
        result = get_companies_names_price_earnings()
        stocks = take_one_stock(result)
        for i in range(15):  # filling 15 stocks
            stock = stocks.__next__()
            write_stock(stock)

    fill_one_financial('adasdad', year=2000)  # filling financial for a specific year
    #get_all_financials('ADBE')
