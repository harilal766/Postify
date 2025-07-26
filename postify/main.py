from postify.database_managing.database import SessionLocal
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from .database_managing.database import get_db
from .database_managing.models import Scheduled_Order
from .shopify.shopify_order import Shopify
from .environment_variables import *
from .response import Tracking_Response

app = FastAPI()

class Order:
    pass


@app.get("/orders",status_code = 200)
def read_orders(db: Session = Depends(get_db)):
    try:
        orders = db.query(Scheduled_Order).all()
    except Exception as e:
        print(e)
    else:
        return orders

@app.get("/orders/{identification}",status_code = 200)
def read_order(identification : str, db:Session = Depends(get_db)):
    order_response = None
    status = None; sh_inst = Shopify(identification=identification)
    try:
        # input sanitization
        if identification[0] == "#":
            identification = identification.strip("#")
        elif len(identification) == 10:
            #identification = 
            print(identification)
        scheduled_order = db.query(Scheduled_Order).filter(
            (Scheduled_Order.Mobile == identification) | 
            (Scheduled_Order.Order_ID == f"#{identification}")    
        ).all()
        
        if scheduled_order:
            status = "Found in scheduled orders."
            scheduled_order = scheduled_order[-1]
            order_response = {
                "Name" : scheduled_order.Name,
                "Order_id" : scheduled_order.Order_ID,
                "Mobile" : scheduled_order.Mobile,
                "Status" : f"Scheduled, Tracking Id : {scheduled_order.Barcode}",
            }
        else:
            unscheduled_order = sh_inst.search_in_all_unscheduled_stores()
            node = unscheduled_order.get("node",None)
            if node:
                status = "Found in unscheduled orders"
                order_response = {
                    "Order_id" : node["name"],
                    "Status" : f"Confirmed, {node["displayFulfillmentStatus"].capitalize()}."
                }
            else:
                raise HTTPException(
                    status_code=404, detail="Order Not Found"
                )
            
        print(status)
    except Exception as e:
        print(f"Order detail error : {e}")
    else:
        return order_response


