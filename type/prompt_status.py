from enum import Enum


class PromptStatus(Enum):
    NOT_STARTED="NOT_STARTED"
    IN_PROGRESS="IN_PROGRESS"
    COMPLETE="COMPLETE"
    ERROR="ERROR"