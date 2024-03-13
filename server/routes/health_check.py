from flask import request, Blueprint
import os 

# app = Flask(__name__)
bp = Blueprint('health_check', __name__)
@bp.route('/health_check', methods=['POST'])
async def health_check():
    return {"status": 200, "message": "Server is up and running"}



