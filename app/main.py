import os
from fastapi import FastAPI, Depends, HTTPException, status, Header
from fastapi.middleware.cors import CORSMiddleware
import json
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
import logging
import sys

load_dotenv()

from app.functions import format_query_json, triage, age_out, triage_with_age_out
from app.logging_config import setup_logging

from app import routes

logger = setup_logging()

app = FastAPI(title = 'Colonoscopy triage API')

ORIGINS = os.getenv('CORS_ORIGINS', '').split(',')

app.add_middleware(
    CORSMiddleware,
    allow_origins = ORIGINS,
    allow_credentials = False,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
# def verify_api_key(x_api_key: str = Header(...)):
#     if x_api_key != os.getenv('MY_API_KEY'):
#         raise HTTPException(
#             status_code = status.HTTP_401_UNAUTHORIZED,
#             detail = 'Invalid or missing API key'
#         )

class UserInput(BaseModel):
    user_query: str


app.include_router(routes.router)


    
