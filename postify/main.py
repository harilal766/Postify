from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Request, Form,UploadFile,File, APIRouter
from fastapi.security import OAuth2PasswordBearer

from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware
from .database_managing.models import *
from .shopify.shopify_order import Shopify
from .environment_variables import *
from .response import Tracking_Response
from .security import verify_api_key
from .utils import html_reader
import re, uvicorn
from pprint import pprint
from jinja2 import Environment, PackageLoader, select_autoescape


import pandas as pd
from io import StringIO

class Order:
    def __init__(self):
        self.base_url = '/orders/'
        
    def get_order(self,identification : str):
        order_response = {
            "Name" : None,"Order_id" : None,
            "Mobile" : None,"Status" : None
        }
        status = None; sh_inst = Shopify(order_id=identification)
        try:
            scheduled_order = Scheduled_Order().find_scheduled_order(id=identification)
            if scheduled_order:
                order_response["Name"] = scheduled_order.Name
                order_response["Order_id"] = scheduled_order.Order_ID
                order_response["Mobile"] = scheduled_order.Mobile
                
                order_response.update({
                    "Speedpost Tracking Id" : scheduled_order.Barcode,
                })
                order_response.update({
                    "Scheduled on " : scheduled_order.Entry_Date
                })
                # Order Status
                if scheduled_order.is_despatched_and_bagged() == True:
                    third_party = f"https://www.aftership.com/track/india-post/{scheduled_order.Barcode}"
                    indiapost = "https://www.indiapost.gov.in"
                    order_response['Status'] = f"Tracking : {third_party}"
                elif scheduled_order.is_despatched_and_bagged() == False:
                    order_response["Status"] = "Scheduled, Tracking link will be available soon."  
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
                    order_response["Status"] = f"Order Confirmed, will Despatch on next working day."
                else:
                    status = 404
            return order_response
        except Exception as e:
            print(f"Order detail error : {e}")
            
    def order_page(self, request : Request, identification : str):
        track = Tracking()
        try:
            return track.show_tracking_page(request=request,identification=identification)
        except Exception as e:
            print(f"Order page error : {e}")

class Pickup:
    def __init__(self):
        self.base_url = "/pickup/"
        
    def missing_form(self,request:Request):
        entry_dates = Scheduled_Order().find_all_entry_timestamps()
        context = {
            "timestamps" : reversed([timestamp[0] for timestamp in entry_dates])
        }
        try:
            return templates.TemplateResponse(
                request=request, name="missing_form.html", context = context
            )
        except Exception as e:
            print(e)

    async def find_missing_orders(self,request : Request,
        selected_entries:list[str]=Form(),
        scanned_csv:UploadFile = File()
        ):
        scheduled = Scheduled_Order()
        context = {
            "scanned_barcodes" : None, "unscanned_orders" : None,
            "selected_entries" : None
        }
        try:
            file_contents = await scanned_csv.read()
            decoded = file_contents.decode("utf-8")
            scanned_df = pd.read_csv(
                StringIO(decoded)
            )
            scanned_barcodes = scanned_df["name"].to_list()
            
            context["unscanned_orders"] = scheduled.find_unscanned_orders(
                scanned_barcodes=scanned_barcodes,
                selected_entry_dates=selected_entries
            )
            context["scanned_barcodes"] = sorted(scanned_barcodes)
            context["selected_entries"] = selected_entries[::-1]

            return templates.TemplateResponse(request=request, name="unscanned.html", context=context) 
        except Exception as e :
            return templates.TemplateResponse(request=request, name="error.html", context= {"error" : "Required parameters not selected"}) 

class Tracking:
    def __init__(self):
        self.base_url = "/track"
        
    def tracking_form(self,request: Request):
        try:
            return templates.TemplateResponse(
                request=request, name="tracking_form.html"
            )
        except Exception as e:
            print(e)
    
    def show_tracking_page(self,request : Request, identification):
        order = Order().get_order(identification=identification)
        try:
            if not order:
                pass
            
            if "https" in order["Status"]:
                tracking_id = order.get("Speedpost Tracking Id",None)
                if tracking_id:
                    return RedirectResponse(url=f"https://www.aftership.com/track/india-post/{tracking_id}")
            else:
                tracking_id_pattern = r'^EL\d{9}IN'
                link_pattern = r'https://.*'
                for key,value in order.items():
                    if value != None:
                        link_matches = re.search(link_pattern,value)
                        tracking_id_matches = re.match(tracking_id_pattern,value)
                        
                        if link_matches:
                            matched_link = link_matches.group()
                            value = value.replace(
                                matched_link, 
                                f"<a target='_blank' href='{matched_link}'>{matched_link.strip("https://www.")}</a>"
                            )
                            
                        if tracking_id_matches:
                            matched_tracking_id = tracking_id_matches.group()
                            tag = 'span'
                            value = value.replace(
                                matched_tracking_id, 
                                f"<{tag} type='text' class='copy'>{matched_tracking_id}</{tag}>"
                            )
                        
                        order[key] = value
                return templates.TemplateResponse(request=request, name="tracking_result.html", context={"order" : order}) 
        except Exception as e:
            print(e)
            
    def track_order(self,request: Request ,order_id:str=Form()):
        tracked_order = None
        try:
            tracked_order = self.show_tracking_page(request=request,identification=order_id)
        except Exception as e:
            print(e)
        return tracked_order

router = APIRouter()
# Endpoints 
order = Order() 
router.add_api_route(order.base_url + "{identification}",order.get_order,methods=["GET"])
router.add_api_route(order.base_url + "{identification}/html",order.order_page,methods=["GET"])

pickup = Pickup()
router.add_api_route(pickup.base_url + "missing_form", pickup.missing_form,methods=["GET"])
router.add_api_route(pickup.base_url + "find_missing", pickup.find_missing_orders,methods=["POST"])


tracking = Tracking()
router.add_api_route(tracking.base_url, tracking.tracking_form,methods=["GET"])
router.add_api_route(tracking.base_url , tracking.track_order, methods=["POST"])
router.add_api_route(tracking.base_url + "/{identification}", tracking.show_tracking_page, methods=["GET"])



app = FastAPI()
app.include_router(router)

app.add_middleware(
    CORSMiddleware,allow_origins = ALLOWED_ORIGINS,allow_credentials = True,
    allow_methods = ["GET"],allow_headers = ["*"],
)

app.mount("/postify/static", StaticFiles(directory="postify/static"), name="postify_static")
templates = Jinja2Templates(directory="postify/templates")

