from sqlalchemy import Column, Integer, String
from database import Base


class URLs(Base):
    __tablename__ = 'urls'

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String)
    url = Column(String)
