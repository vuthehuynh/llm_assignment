from pydantic import BaseModel
from typing import List, Optional, Text, Dict, Any

class QnAInput(BaseModel):
    prompt: Text
    pdf_path: Text
    user_id: Text