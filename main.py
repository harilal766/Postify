from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from environment_variables import *
import sqlitecloud

connection = sqlitecloud.connect(DB_ACCESS["connection"])

cursor = connection.execute(f"SELECT * FROM {DB_ACCESS["tablename"]}")

result = cursor.fetchall()


print(result)