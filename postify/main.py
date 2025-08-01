from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from .database_managing.database import get_db
from .database_managing.models import Scheduled_Order
from .shopify.shopify_order import Shopify
from .environment_variables import *
from .response import Tracking_Response
from .security import verify_api_key
from .utils import html_reader
from urllib.parse import unquote
import re
from pprint import pprint

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

app = FastAPI()

"""
app.add_middleware(
    CORSMiddleware,allow_origins = ["*"],allow_credentials = True,
    allow_methods = ["GET"],allow_headers = ["*"],
)
"""

@app.get("/orders/{identification}/html",status_code = 200)
def read_order(identification : str, db:Session = Depends(get_db)):
    order_response = {
        "Name" : None,"Order_id" : None,
        "Mobile" : None,"Status" : None
    }
    status = None; sh_inst = Shopify(identification=identification)
    try:
        print(unquote(identification))
        # input sanitization
        if identification[0] == "#":
            identification = identification.lstrip("#")
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
            
            order_response["Name"] = scheduled_order.Name
            order_response["Order_id"] = scheduled_order.Order_ID
            order_response["Mobile"] = scheduled_order.Mobile
            order_response["Status"] = f"Scheduled, Track on : https://app.indiapost.gov.in/enterpriseportal/track-result/article-number/{scheduled_order.Barcode}"

        else:
            unscheduled_order = sh_inst.search_in_all_unscheduled_stores()
            print(unscheduled_order)
            node = unscheduled_order.get("node",None)
            if node:
                customer = node.get("billingAddress",None)
                status = "Found in unscheduled orders"
                if customer:
                    order_response["Name"] = customer["name"]
                    order_response["Mobile"] = customer["phone"]
                order_response["Order_id"] = node["name"]
                order_response["Order date"] =  node["createdAt"].split("T")[0]
                order_response["Status"] = f"Confirmed, {node["displayFulfillmentStatus"].capitalize()}."
            else:
                return HTTPException(
                    status_code=404, detail="Order Not Found"
                )
                
            
    except Exception as e:
        print(f"Order detail error : {e}")
    else:
        html_template = html_reader("tracking_template.html")
        for key,value in order_response.items():
            print(key,value)
            if value != None and "https" in value:
                value_split = value.split(" ")
                value_split[-1] = f"<a href='{value_split[-1]}' target='_blank'>Click</a>"
                value = ' '.join(value_split)
            
            html_template = html_template.replace(f"<td>{key}</td>",f"<td>{value}</td>",)
        
        return HTMLResponse(content = html_template, status_code=200)


