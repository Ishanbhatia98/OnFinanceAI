
from typing import Dict, Tuple

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, validator
from schema.prompt_log import PromptRequest, PromptResponse, EditPromptLog
from model.prompt_log import PromptLog
from bson import ObjectId
import threading
from type.prompt_status import PromptStatus

def generate_response_from_user_prompt(prompt_log_id:str)->Tuple[str, Dict]:
    prompt_log = PromptLog.get_or_404(id=prompt_log_id)
    prompt_log.update(status=PromptStatus.IN_PROGRESS)
    try:
        response, exhaustive_response = '', {}
        PromptLog.edit(id=prompt_log.id, edit_log=EditPromptLog(response=response, exhaustive_response= exhaustive_response))
    except Exception as e:
        prompt_log.error = {'msg':str(e)}
        prompt_log.save()



class QueryJobQueue:
    def __init__(self):
        # self.active_queries = 0
        self.pending_queries = []
        self.max_concurrent_request = 10
        
    
    @property
    def active_queries(self):
        return int(PromptLog.objects(status=PromptStatus.IN_PROGRESS).count())
    
    
    def run_job(self, prompt_log_id:ObjectId):
        threading.Thread(target=generate_response_from_user_prompt, args=(prompt_log_id))        
    

    def add_query_job(self, prompt_log_id:ObjectId):
        self.pending_queries.append(prompt_log_id)
        
    
    def run_on_loop(self):
        while True:
            print('Active Queries: ', self.active_queries)
            print('Pending Queries: ', self.pending_queries)
            if self.active_queries <= self.max_concurrent_request:
                if self.pending_queries:
                    prompt_log_id = self.pending_queries.pop()
                    # threading.Thread(target=func).start()
                    self.run_job(prompt_log_id)
                    

query_job_queue = QueryJobQueue()


                