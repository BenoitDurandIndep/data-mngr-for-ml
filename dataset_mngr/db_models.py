from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Symbol(Base):
    __tablename__ = 'SYMBOL'
    SK_SYMBOL = Column(Integer, primary_key=True, autoincrement=True)
    CODE = Column(Text)
    NAME = Column(Text)
    TYPE = Column(Text)
    REGION = Column(Text)
    CURRENCY = Column(Text)
    COMMENT = Column(Text)
    CODE_ALPHA = Column(Text)
    CODE_YAHOO = Column(Text)
    CODE_ISIN = Column(Text)