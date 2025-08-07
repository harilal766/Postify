from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware
from .database_managing.models import Scheduled_Order
from .shopify.shopify_order import Shopify
from .environment_variables import *
from .response import Tracking_Response
from .security import verify_api_key
from .utils import html_reader
import re, uvicorn
from pprint import pprint
from jinja2 import Environment, PackageLoader, select_autoescape


app = FastAPI()
app.add_middleware(
    CORSMiddleware,allow_origins = ALLOWED_ORIGINS,allow_credentials = True,
    allow_methods = ["GET"],allow_headers = ["*"],
)
templates = Jinja2Templates(directory="postify/templates")

@app.get("/orders/{identification}")
def get_order(identification : str):
    order_response = {
        "Name" : None,"Order_id" : None,
        "Mobile" : None,"Status" : None
    }
    status = None; sh_inst = Shopify(identification=identification)
    try:
        scheduled_order = Scheduled_Order().find_scheduled_order(id=identification)
        if scheduled_order:
            order_response["Name"] = scheduled_order.Name
            order_response["Order_id"] = scheduled_order.Order_ID
            order_response["Mobile"] = scheduled_order.Mobile
            order_response.update({
                "Speedpost Tracking Id" : scheduled_order.Barcode,
                "Scheduled on " : scheduled_order.Entry_Date
            })
            order_response["Status"] = f"Scheduled, track <strong>{scheduled_order.Barcode}</strong> on : https://www.indiapost.gov.in"
        else:
            unscheduled_order = sh_inst.search_in_all_stores()
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
        return order_response
    except Exception as e:
        print(f"Order detail error : {e}")

@app.get("/orders/{identification}/html",status_code = 200, response_class=HTMLResponse)
def order_page(request : Request, identification : str):
    order = None
    try:
        order = get_order(identification=identification)
        if order:
            status = 200
            
            link_matches = re.search(r'https://[^\s\#]*',order["Status"])
            if link_matches:
                matched_link = link_matches.group()
                order["Status"] = order["Status"].replace(matched_link, f"<a target='_blank' href='{matched_link}'>{matched_link.strip("https://www.")}</a>")
        else:
            status = 404
        return templates.TemplateResponse(request=request, name="tracking_result.html", context={"order" : order}) 
        #return HTMLResponse(content=html_template,status_code=status)
    except Exception as e:
        print(f"Order detail error : {e}")