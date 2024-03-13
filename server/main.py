import sys
from pathlib import Path
from flask import Flask, request, jsonify
sys.path.append(Path(__file__).parent.absolute().as_posix())
from routes import upload_file, chat, health_check
from settings import settings


app = Flask(__name__)

# Register blueprints
app.register_blueprint(upload_file.bp)
app.register_blueprint(chat.bp)
app.register_blueprint(health_check.bp)


if __name__ == "__main__":
    # In production, don't forget to change reload => False
    app.run(host='localhost', port=settings.API_PORT)
