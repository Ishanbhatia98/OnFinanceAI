
from pydantic import BaseModel, root_validator
from secrets import token_hex
from typing import Optional, Dict
from type.prompt_status import PromptStatus
from bson import ObjectId

def to_orm_dict(d):
    if isinstance(d, dict):
        return {k: to_orm_dict(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [to_orm_dict(v) for v in d]
    elif isinstance(d, ObjectId) and ObjectId.is_valid(d):
        return str(d)
    else:
        return d
    

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ReversePyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        # if not ObjectId.is_valid(v):
        #     raise ValidationError("Invalid objectid")
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")



class PromptRequest(BaseModel):
    conversation_id: Optional[str]
    query: str
    
    @root_validator
    def validate_prompt_request(cls, values):
        if values.get("conversation_id") is None:
            values['conversation_id'] = token_hex(6)

class EditPromptLog(BaseModel):
    query:Optional[str]
    response: Optional[str]
    exhaustive_response: Optional[Dict]


class PromptResponse(PromptRequest, orm_mode=True):
    id: ReversePyObjectId
    response: str
    status:PromptStatus
    

        
    