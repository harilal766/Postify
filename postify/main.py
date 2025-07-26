from postify.database_managing.database import SessionLocal
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .database_managing.database import get_db
from .database_managing.models import Scheduled_Order
from .shopify.shopify_order import Shopify
from .environment_variables import *

app = FastAPI()

@app.get("/orders")
def read_orders(db: Session = Depends(get_db)):
    try:
        orders = db.query(Scheduled_Order).all()
    except Exception as e:
        print(e)
    else:
        return orders

@app.get("/orders/{identification}")
def read_order(identification : str, db:Session = Depends(get_db)):
    order_response = None; sh_inst = Shopify(identification=identification)
    try:
        # input sanitization
        if identification[0] == "#":
            identification = identification.strip("#")
        elif len(identification) == 10:
            identification = identification.strip()
            print(identification, identification[:-10])
            
        scheduled_order = db.query(Scheduled_Order).filter(
            (Scheduled_Order.Mobile == identification) | 
            (Scheduled_Order.Order_ID == f"#{identification}")    
        ).all()[-1]
        
        if scheduled_order:
            order_response = scheduled_order
        else:
            # add shopify api access here
            unscheduled_order = sh_inst.handle_stores()
            
            print(unscheduled_order)
                
            raise HTTPException(
                status_code=404, detail="Order Not Found"
            )
    except Exception as e:
        print(e)
    else:
        return order_response


