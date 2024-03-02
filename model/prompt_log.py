

import os
import threading
from contextlib import contextmanager
from copy import deepcopy
from unittest.mock import patch

import mongoengine as me
import requests
from bson import ObjectId
from typeguard import typechecked
from datetime import datetime
from fastapi import HTTPException
from schema.prompt_log import PromptRequest, EditPromptLog
from type.prompt_status import PromptStatus



@typechecked
class CreatedAtUpdatedAtMixin(me.Document):
    meta = {"abstract": True}
    created_at = me.DateTimeField(default=datetime.utcnow, required=True)
    updated_at = me.DateTimeField(default=datetime.utcnow, required=True)

@typechecked
class GetOr404Mixin:
    @classmethod
    def get_or_404(cls, **kwargs):
        if "deleted_at" in cls._fields:
            obj = cls.objects(**kwargs, deleted_at=None).first()
        else:
            obj = cls.objects(**kwargs).first()
        if obj is None:
            raise HTTPException(
                status_code=404, detail=f"{cls.__name__} with id {kwargs} not found"
            )
        return obj

    @classmethod
    def get_or_none(cls, **kwargs):
        if "deleted_at" in cls._fields:
            return cls.objects(**kwargs, deleted_at=None).first()
        return cls.objects(**kwargs).first()



class PromptLog(GetOr404Mixin, CreatedAtUpdatedAtMixin):
    id = me.ObjectIdField(primary_key=True, default=ObjectId)
    conversation_id = me.StringField(required=True)
    query = me.StringField(required=True)
    response = me.StringField()
    status= me.EnumField(PromptStatus, default=PromptStatus.NOT_STARTED)
    exhaustive_response = me.DictField()
    error = me.DictField()
    
    def save(self):
        if self.response is not None:
            self.status = PromptStatus.COMPLETE
        if self.error:
            self.status = PromptStatus.ERROR
        return super().save()
    
    
        
    @classmethod
    def create(cls, request:PromptRequest)->"PromptLog":
        return cls(**request.dict(exclude_unset=True)).save()
    
    @classmethod
    def edit(cls, id:ObjectId, edit_log:EditPromptLog):
        return cls.update(**edit_log.dict(exclude_unset=True))
    
    


if __name__ == "__main__":
    print('Init')