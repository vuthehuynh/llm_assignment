from flask import request, Blueprint
import sys 
from pathlib import Path
sys.path.append(Path(__file__).parent.absolute().as_posix())
from services.ragqna_service import raq_qna_service
from schemas import QnAInput

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['POST'])
async def chat_handle():
    inputdata = QnAInput.parse_obj(dict(request.form))
    response = await raq_qna_service.chat(inputdata)
    return response