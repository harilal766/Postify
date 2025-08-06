from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import HTMLResponse, JSONResponse
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
import re, uvicorn
from pprint import pprint

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,allow_origins = ALLOWED_ORIGINS,allow_credentials = True,
    allow_methods = ["GET"],allow_headers = ["*"],
)

@app.get("/orders/{identification}")
def get_order(identification : str, db:Session = Depends(get_db)):
    order_response = {
        "Name" : None,"Order_id" : None,
        "Mobile" : None,"Status" : None
    }
    status = None; sh_inst = Shopify(identification=identification)
    try:
        # input sanitization
        if len(identification) >= 10:
            scheduled_order = db.query(Scheduled_Order).filter(
                Scheduled_Order.Mobile == identification     
            ).all()
        else:
            if identification[0] == "#":
                identification = identification.lstrip("#")
            scheduled_order = db.query(Scheduled_Order).filter(
                Scheduled_Order.Order_ID == f"#{identification}"    
            ).all()
            
        if scheduled_order:
            status = "Found in scheduled orders."
            scheduled_order = scheduled_order[-1]
            
            order_response["Name"] = scheduled_order.Name
            order_response["Order_id"] = scheduled_order.Order_ID
            order_response["Mobile"] = scheduled_order.Mobile
            order_response.update({
                "Speedpost Tracking Id" : scheduled_order.Barcode
            })
            order_response["Status"] = f"Scheduled, track <strong>{scheduled_order.Barcode}</strong> on : https://www.indiapost.gov.in"

            
        else:
            unscheduled_order = sh_inst.search_in_all_unscheduled_stores()
            status = 200
            if unscheduled_order:
                unscheduled_order = unscheduled_order.get("node",None)
                customer = unscheduled_order.get("billingAddress",None)
                status = "Found in unscheduled orders"
                if customer:
                    order_response["Name"] = customer["name"]
                    order_response["Mobile"] = customer["phone"]
                order_response["Order_id"] = unscheduled_order["name"]
                order_response["Order date"] =  unscheduled_order["createdAt"].split("T")[0]
                order_response["Status"] = f"Confirmed, {unscheduled_order["displayFulfillmentStatus"].capitalize()}."
            else:
                status = 404
                order_response = "Order Not Found"
    except Exception as e:
        print(f"Order detail error : {e}")
    else:
        return JSONResponse(content = order_response, status_code = status)

@app.get("/orders/{identification}/html",status_code = 200)
def order_page(identification : str, db:Session = Depends(get_db)):
    order = None
    try:
        order = get_order(identification=identification, db=db)
        if order.status_code == 200:
            status = 200
            html_template = html_reader("tracking_template.html")
            tab = "    "
            table_placeholder = "{{TABLE}}"
            table_placeholder_match = re.search(fr'{tab}?{table_placeholder}',html_template)
            tab_count  = re.search(tab,table_placeholder_match.group())
            table_start = f'<table class="table table-bordered table-striped table-rounded">\n'
            table_end = '</table>'
            for key,value in order.items():
                if value:
                    link_matches = re.findall(r'https://[^\s\#]*',value)
                    for link in link_matches:
                        if len(link) > 0:
                            value = value.replace(link, f"<a target='_blank' href='{link}'>{link}</a>")
                    table_start += f"{tab*4}<tr><th>{key}</th><td>{value}</td></tr>\n"
            html_template = html_template.replace(table_placeholder,f"{table_start}{tab*3}{table_end}",)
        else:
            status = 404
            html_template = html_reader("no_order.html")
        return HTMLResponse(content = html_template, status_code=status)
    except Exception as e:
        print(f"Order detail error : {e}")