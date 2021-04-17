from datetime import datetime
from sqlalchemy import (
Table,
MetaData,
Column,
Integer,
String,
Boolean,
create_engine,
DateTime,
func
)
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base



# users_table = Table(
#     'users',
#     metadata,
#     Column('id',Integer,primary_key=True),
#     Column('username',String(30),unique=True),
#     Column('is_staff',Boolean,nullable=False,default=False), # oly 1 or 0
# )

engine = create_engine('sqlite:///example03.db',echo=True)

Base = declarative_base(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True)
    username = Column(String(32),unique=True)
    is_staff = Column(Boolean,nullable=False,default=False,server_default='0')
    created_at = Column(DateTime,nullable=False,default=datetime.utcnow,server_default=func.now())

if __name__ == '__main__':
    Base.metadata.create_all()
