from sqlalchemy import (
Table,
MetaData,
Column,
Integer,
String,
Boolean,
create_engine
)
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///example01.db',echo=True)
metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('username',String(30),unique=True),
    Column('is_staff',Boolean,nullable=False,default=False), # oly 1 or 0
)

class User:
    def __init__(self,id: int,username:str,is_staff:bool = False):
        """
        :param id:
        :param username:
        :param is_staff:
        """
        self.id = id
        self.username = username
        self.is_staff = is_staff
#
# if __name__ == '__main__':
#     metadata.create_all(engine)

mapper(User,users_table)
