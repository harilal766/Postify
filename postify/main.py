
from typing import Annotated
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database_managing.database import get_db
from .database_managing.models import Scheduled_Order
from .shopify.shopify_order import Shopify
from .environment_variables import *
from .response import Tracking_Response
from .security import verify_api_key
app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")


class Order:
    pass


@app.get("/orders",status_code = 200)
def read_orders(db: Session = Depends(get_db),api_key:str=Depends(verify_api_key)):
    try:
        orders = db.query(Scheduled_Order).all()
    except Exception as e:
        print(e)
    else:
        return orders

@app.get("/orders/{identification}",status_code = 200)
def read_order(identification : str, db:Session = Depends(get_db),api_key:str=Depends(verify_api_key)):
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
                "Status" : f"Scheduled, Track on : https://app.indiapost.gov.in/enterpriseportal/track-result/article-number/{scheduled_order.Barcode}"
            }

        else:
            unscheduled_order = sh_inst.search_in_all_unscheduled_stores()
            node = unscheduled_order.get("node",None)
            if node:
                status = "Found in unscheduled orders"
                order_response = {
                    "Order_id" : node["name"],
                    "Order date" : node["createdAt"].split("T")[0],
                    "Status" : f"Confirmed, {node["displayFulfillmentStatus"].capitalize()}."
                }
            else:
                return HTTPException(
                    status_code=404, detail="Order Not Found"
                )
                
            
    except Exception as e:
        print(f"Order detail error : {e}")
    else:
        return order_response


