from flask import Flask
from flask_cors import CORS
from routes.words import words_bp
from routes.health import health_bp
from services.word_service import _words_data as words_data

app = Flask(__name__)
CORS(app)

app.register_blueprint(words_bp, url_prefix='/api/words')
app.register_blueprint(health_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
