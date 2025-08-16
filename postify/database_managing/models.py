from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, declarative_base

from ..environment_variables import order_table,db_connection

from sqlalchemy import create_engine,select,func
from postify.shopify.shopify_order import Shopify
import re
engine = create_engine(db_connection)

import pandas as pd
Base = declarative_base()

class Scheduled_Order(Base):
    __tablename__ = order_table
    Trans_ID = Column(Integer, primary_key=True)
    Order_ID = Column(String,index=True)
    Name = Column(String)
    Barcode = Column(String)
    Mobile = Column(String)
    Products = Column(String)
    Entry_Date = Column(String)
    
    def __str__(self):
        return self.Order_ID
    
    def find_scheduled_order(self,id:str):
        try:
            sh = Shopify(order_id=id)
            if re.match(sh.order_id_pattern,id):
                order = sh.search_in_all_stores()
                if order:
                    order_id = order['node']['name']
                    id = order_id
                    print(id,)
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
            
    @classmethod
    def filtered_shipment(cls, entry_date:str):
        orders = None
        try:
            with Session(engine) as session:
                orders = session.query(cls).filter(
                    func.date(cls.Entry_Date) == entry_date
                ).all()
        except Exception as e:
            print(e)
        else:
            return orders


