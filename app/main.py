import os
from fastapi import FastAPI, Depends, HTTPException, status, Header
import json
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
import logging
import sys

load_dotenv()

from app.functions import format_query_json, triage
from app.logging_config import setup_logging

logger = setup_logging()

app = FastAPI(title = 'Colonoscopy triage API')


def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != os.getenv('MY_API_KEY'):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = 'Invalid or missing API key'
        )

class UserInput(BaseModel):
    user_query: str


@app.post('/triage', dependencies = [Depends(verify_api_key)])
async def recommend(request: UserInput):
    user_query = request.user_query
    json_summary = await format_query_json(user_query)
    recommendation = triage(json_summary)

    logger.info("User input received and recommendation generated", 
                extra = {
                    'extra_data': {
                        'user_input': user_query,
                        'json_summary': json_summary,
                        'recommendation': recommendation
                    }
                }

    )

    return {'user_input': json_summary, 'recommendation': recommendation}


    
