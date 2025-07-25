from postify.database import SessionLocal
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session
from .database import get_db
from postify.models import Order

app = FastAPI()



@app.get("/orders")
def read_orders(db: Session = Depends(get_db)):
    try:
        orders = db.query(Order).all()
    except Exception as e:
        print(e)
    else:
        return orders


@app.get("/orders/{order_id}")
def read_order(order_id : str, db:Session = Depends(get_db)):
    try:
        order = db.query(Order).filter(
            Order.Order_ID == order_id
        ).first()
        
        if not order:
            raise HTTPException(
                status_code=404, detail="Order Not Found"
            )
    except Exception as e:
        print(e)
    else:
        return order
    
