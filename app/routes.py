from fastapi import APIRouter, File, UploadFile, HTTPException
from pydantic import BaseModel
import logging

from app import functions
from app.logging_config import setup_logging

logger = setup_logging()

router = APIRouter(tags=['triage'])


class UserInput(BaseModel):
    user_query: str


@router.post("/triage")
async def recommend(request: UserInput):
    user_query = request.user_query
    #redacted_user_query = functions.redact_pii(user_query)
    json_summary = await functions.format_query_json(user_query)
    recommendation = functions.triage(json_summary)
    final = functions.triage_with_age_out(json_summary, recommendation)

    logger.info("User input received and recommendation generated", 
                extra = {
                    'extra_data': {
                        'user_input': user_query,
                        'json_summary': json_summary,
                        'recommendation': recommendation
                    }
                }

    )

    return {'user_input': json_summary, 'recommendation': final}