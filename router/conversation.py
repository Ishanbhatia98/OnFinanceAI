from typing import Dict, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from schema.prompt_log import PromptRequest, PromptResponse, EditPromptLog, PyObjectId
from model.prompt_log import PromptLog
from core.query_job import query_job_queue
router = APIRouter(tags=["Conversation"], dependencies=[])

    
@router.post("/conversation/query", response_model=Dict, status_code=status.HTTP_201_CREATED)
def attend_prompt_request(request: PromptRequest):
    log = PromptLog.create(request)
    query_job_queue.add_query_job(log.id)
    log.reload()
    return log


@router.get("/conversation/query/{id}", response_model=Dict, status_code=status.HTTP_201_CREATED)
def fetch_prompt_response(id: PyObjectId):
    return PromptLog.get_or_404(id=id)
   