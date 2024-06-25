from typing import Optional
from pydantic import BaseModel

class MessageRequest(BaseModel):
    user_id: Optional[str] =None
    intent: Optional[str]=None
    message: Optional[str]=None