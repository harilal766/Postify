from .database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session

from ..environment_variables import order_table,db_connection

from sqlalchemy import create_engine,select
engine = create_engine(db_connection)


class Scheduled_Order(Base):
    __tablename__ = order_table
    Trans_ID = Column(Integer, primary_key=True)
    Order_ID = Column(String,index=True)
    Name = Column(String)
    Barcode = Column(String)
    Mobile = Column(String)
    Products = Column(String)
    Entry_Date = Column(String)
    
    @classmethod
    def find_scheduled_order(cls,id:str):
        try:
            with Session(engine) as session:
                orders = session.scalars(
                    select(cls).where(
                        (cls.Order_ID == id) | (cls.Mobile == id)
                    )
                ).all()
                if orders:
                    return orders[-1]
        except Exception as e:
            print(e)

