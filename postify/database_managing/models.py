from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String


from ..environment_variables import order_table

class Order(Base):
    __tablename__ = order_table
    Trans_ID = Column(Integer, primary_key=True)
    Order_ID = Column(String)
    Name = Column(String)
    Barcode = Column(String)
    Mobile = Column(String)
    