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

engine = create_engine('sqlite:///example04.db', echo=True)
Base = declarative_base(bind=engine)

session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)


class User(Base):
    __tablename__ = 'users'

    def __init__(self, username='default', is_staff=False):
        self.username = username
        self.is_staff = is_staff

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True)
    is_staff = Column(Boolean, nullable=False, default=False, server_default='0')
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow, server_default=func.now())

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id},username={self.username!r},if_staff={self.is_staff!r},created_at={self.created_at!r} )"

    def __repr__(self):
        return str(self)

    posts = relationship("Post", back_populates="user")

    def get_posts(self):
        post = self.posts
        return post


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(64), nullable=False, default='', server_default='')
    refer_user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return f"{self.__class__.__name__}(id = {self.id},title={self.title!r},user={self.user!r})"

    def __repr__(self):
        return str(self)

    user = relationship(User, back_populates="posts")


def get_companies():
    file = os.path.join(os.getcwd(), 's-and-p-500-companies-financials', 'data', 'constituents-financials.csv')
    companies_ticker = []
    companies_name = []
    print('file path:', file)
    count = 0
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        next(spamreader)
        for row in spamreader:
            # print(', '.join(row))
            companies_ticker.append(row[0])
            companies_name.append([row[1]])
            count += 1
    return companies_name


def create_user(name: str, is_staff: bool = False)-> bool:
    session = Session()
    username = name
    try:
        user = User(username=username, is_staff=is_staff)
        session.add(user)
        session.commit()
        session.close()
        return 1
    except sqlalchemy.exc.IntegrityError as eerr:
        print('There was an error:', eerr)
        session.close()
        return 0




def create_post(username, post: str = ''):
    session = Session()
    user: User = session.query(User).filter_by(username=username).one_or_none()
    print('fetching user:', user)
    print(f"{username} posts before:", user.posts)
    post = Post(title=post, refer_user_id=user.id)
    session.add(post)
    session.commit()
    print('users post:', post)
    print('post after', user.posts)
    session.close()


def get_post(user_name: str):
    session = Session()
    user: User = session.query(User).filter_by(username=user_name).one_or_none()
    out = user.posts
    print(out)
    session.close()
    return out


if __name__ == '__main__':
    # Base.metadata.create_all()
    # name = get_companies()
    # for i in name:
    #    print(*i)
    # for name0 in name:
    #    create_user(*name0,False)
    # a=create_user('Alex',False)
    # create_user('Admin',True)
    create_user('Alex', False)
    # create_post('Admin','somepost')
    # print('result:',get_post('Admin'))
