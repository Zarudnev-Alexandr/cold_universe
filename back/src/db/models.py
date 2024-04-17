from sqlalchemy import Column, Integer, BigInteger, String, Float, Date, ForeignKey, Boolean, DateTime, TIMESTAMP
import datetime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email_code = Column(Integer, nullable=False)
    is_confirmed_email = Column(Boolean, nullable=False, default=False)
    nickname = Column(String, nullable=False)
    tag = Column(String, nullable=False, unique=True)
    level = Column(Integer, nullable=False, default=1)
    exp = Column(Integer, nullable=False, default=0)
    gold = Column(Integer, nullable=False, default=5000)
    gem = Column(Integer, nullable=False, default=200)
    date_of_create = Column(TIMESTAMP(timezone=True), default=datetime.datetime.now())
