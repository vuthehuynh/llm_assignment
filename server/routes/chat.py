from flask import request, Blueprint
import sys 
from pathlib import Path
sys.path.append(Path(__file__).parent.absolute().as_posix())
from services.ragqna_service import raq_qna_service
from schemas import QnAInput

bp = Blueprint('chat', __name__)

@bp.route('/chat', methods=['POST'])
async def chat_handle():
    # prompt = request.form.get('prompt')
    # pdf_path = request.form.get('pdf_path')
    # user_id = request.form.get('user_id')
    # data = **request.form
    inputdata = QnAInput.parse_obj(request.form)
    response = await raq_qna_service.chat(inputdata)
    return response