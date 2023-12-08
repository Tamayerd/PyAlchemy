#pip install sqlalchemy psycopg2
#pip install -U Flask-SQLAlchemy
from sqlalchemy import create_engine  #connection database
from sqlalchemy.orm import DeclarativeBase # DeclarativeBase = tables main class, database assosiacion with py 
from typing import Optional, List
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session, DeclarativeBase
from sqlalchemy import create_engine, text, MetaData, Table, Column, Integer, String, ForeignKey, insert, select, update, delete  #table


### CREATE DATABASE RELATİON ###

from config import DATABASE_URI
engine = create_engine(DATABASE_URI)

class Base(DeclarativeBase): 
    pass




#### CREATE TABLE (ENGINE)#####


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")  #one-to-many, ... = relationship; back_populates = two-side relation, user with address
    
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})" #!r = string format


#One-to-many realtionship#

class Address(Base):
    
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address = {self.email_address!r})"

#create table
# table_objects = [Base.metadata.tables["user_account"], Base.metadata.tables["address"]]

# Base.metadata.create_all(engine, tables=table_objects)

# Address.metadata.create_all(engine) 
# User.metadata.create_all(engine) 



### CREATE OBJECTS AND PERSIST ###

##Alternative##
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()

with Session(engine) as session:             #  Session using for db operations
    spongebob = User(
        name = "sungerbob",
        fullname = "Spongebob Squarepants",
        addresses = [Address(email_address = 'spongebob@sqlalchemy.org')],
    )
    sandy = User(
        name = "sandy",
        fullname = "Sandy Cheeks",
        addresses = [Address(email_address = "sandy@sqlalchemy.org")],

    )
    patric = User(
        name = "patrick",
        fullname = "Patrick Star" 
    )

    # session.add_all([spongebob,sandy,patric])

    # session.commit()



### SELECT (simple) ###

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(engine)

stmt = select(User).where(User.name.in_(["spongebob", "sandy"]))  # in_ => filter operator

# for user in session.scalars(stmt):  # session.scalars => only one colum for query
#     print(user)


### SELECT with JOIN ###

stmt = (
    select(Address)
    .join(Address.user)
    .where(User.name == "sandy")
    .where(Address.email_address == "sandy@sqlalchemy.org")
)

sandy_address = session.scalar(stmt)  # one() => just one conclutions
# print(sandy_address)



### MAKE CHANGES ###

stmt = select(User).where(User.name == "patrick")

# patric = session.scalar(stmt)
# print(patric)


### SOME DELETES ###

sandy = session.get(User, 2)
sandy.addresses.remove(sandy_address)
session.flush() #değişiklikleri göndermeden önce 

