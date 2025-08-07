from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Session, declarative_base

from ..environment_variables import order_table,db_connection

from sqlalchemy import create_engine,select
from postify.shopify.shopify_order import Shopify
import re
engine = create_engine(db_connection)

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
    
    @classmethod
    def find_scheduled_order(cls,id:str):
        """_summary_

        Args:
            id (str): shopify order id or the phone number on the order
            
            find the correct order id with suffixes and prefixes from shopify if any,
            and return it as the value to be queried
            
            query the table with the id, it may return one or more than one results if it exists
            
            it need to be indexed to find the result

        Returns:
            _type_: _description_
        """
        try:
            sh = Shopify(identification=id)
            if re.match(sh.order_id_pattern,id):
                order = sh.search_in_all_stores()
                if order:
                    order_id = order['node']['name']
                    id = order_id
            
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

