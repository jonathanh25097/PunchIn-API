from pydantic import BaseModel, BeforeValidator
from typing import Annotated, List, Optional
from pydantic import BaseModel, Field, validator
from bson import ObjectId
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

from bson import ObjectId

def string_to_objectid(s: str) -> ObjectId:
    """
    Convert a string to a MongoDB ObjectId.

    Args:
    - s (str): The string to convert.

    Returns:
    - ObjectId: The converted ObjectId.

    Raises:
    - ValueError: If the string is not a valid ObjectId.
    """
    if not ObjectId.is_valid(s):
        raise ValueError(f"Invalid ObjectId string: {s}")
    return ObjectId(s)


PyObjectId = Annotated[str, BeforeValidator(str)]
    
class DocumentKey(BaseModel):
    id: PyObjectId = Field(alias='_id', default=None)
    name: str
    
    
class User(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    name: str
    lastName: str
    email: str
    username: str
    password: str 
    phoneNumber: str
    class Config:
        json_encoders = {
            ObjectId: str
        }
    
 
    
class Record(BaseModel):
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    user: DocumentKey
    clockInTime: datetime
    clockOutTime: Optional[datetime] = None
    
   
