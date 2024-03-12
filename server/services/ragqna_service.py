
from flask import request
import sys 
from pathlib import Path
sys.path.append(Path(__file__).parent.absolute().as_posix())

from schemas import QnAInput
from ragqna.app_manager import AppManager

class RagQNAService:
    def __init__(self) -> None:
        self.app_manager = AppManager()

    async def chat(self, data: QnAInput):
        answer = await self.app_manager.chat(data)
        return answer

raq_qna_service = RagQNAService()