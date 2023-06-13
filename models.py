from sqlalchemy import Column, Integer, String

from database import Base

class Selector(Base):
    __tablename__ = 'selectors'

    selector_id = Column(Integer, primary_key=True)
    url = Column(String(50), nullable = False)
    selector = Column(String(50), nullable = False)     
