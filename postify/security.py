from fastapi import HTTPException
from fastapi.security import APIKeyQuery

from .environment_variables import API_KEY

def verify_api_key(api_key: str):
    if api_key != API_KEY:
        raise HTTPException(status_code=403,detail = "Invalid API KEY")
    