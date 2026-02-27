from flask import Flask
from flask_cors import CORS
from routes.words import words_bp
from routes.health import health_bp
from routes.auth import auth_bp
from routes.attempts import attempts_bp
from services.word_service import _words_data as words_data
from services.db_service import init_connection_pool, close_connection_pool
import logging
import os

# Configure logging
# Use ERROR level for production, INFO for development
log_level = logging.ERROR if os.getenv('FLASK_ENV') == 'production' else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = Flask(__name__)
CORS(app)

# Initialize database connection pool
try:
    init_connection_pool()
except Exception as e:
    logging.error(f"Failed to initialize database connection pool: {e}")
    logging.warning("Application starting without database connectivity")

# Register blueprints
app.register_blueprint(words_bp, url_prefix='/api/words')
app.register_blueprint(health_bp)
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(attempts_bp, url_prefix='/api/attempts')

# Note: Connection pool will be closed only on app shutdown (in the finally block below)
# Do NOT close pool after each request (teardown_appcontext runs after EVERY request!)


if __name__ == "__main__":
    try:
        app.run(debug=True, port=5000)
    finally:
        close_connection_pool()
