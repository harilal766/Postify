from postify.database_managing.database import SessionLocal
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .database_managing.database import get_db
from postify.database_managing.models import Order

app = FastAPI()

@app.get("/orders")
def read_orders(db: Session = Depends(get_db)):
    try:
        orders = db.query(Order).all()
    except Exception as e:
        print(e)
    else:
        return orders

@app.get("/orders/{identification}")
def read_order(identification : str, db:Session = Depends(get_db)):
    order = None
    try:
        if len(identification) == 10:
            order = db.query(Order).filter(
                Order.Mobile == identification
            ).first()
        else:
            identification = identification.strip("#")
            order = db.query(Order).filter(
                Order.Order_ID == f"#{identification}"
            ).first()
        

        if not order:
            raise HTTPException(
                status_code=404, detail="Order Not Found"
            )
    except Exception as e:
        print(e)
    else:
        return order
    
