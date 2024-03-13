from flask import request, Blueprint
import os 

bp = Blueprint('upload_file', __name__)

@bp.route('/upload_file', methods=['POST'])
async def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400
    
    file.save(os.path.join('./',  file.filename))
    return "File uploaded successfully", 200