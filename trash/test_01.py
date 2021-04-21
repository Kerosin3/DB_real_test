from sqlalchemy import (
Table,
MetaData,
Column,
Integer,
String,
Boolean,
create_engine
)

engine = create_engine('sqlite:///example01.db',echo=True)
metadata = MetaData()

users_table = Table(
    'users',
    metadata,
    Column('id',Integer,primary_key=True),
    Column('username',String(30),unique=True),
    Column('is_staff',Boolean,nullable=False,default=False), # oly 1 or 0
)

if __name__ == '__main__':
    metadata.create_all(engine)

