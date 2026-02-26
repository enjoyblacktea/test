import logging
import atexit
from flask import Flask
from flask_cors import CORS
from routes.words import words_bp
from routes.health import health_bp
from routes.history import history_bp, init_history_routes
from services.word_service import _words_data as words_data
from services.db_service import DatabaseService
from services.history_service import HistoryService
from config import Config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize database service
db_service = None
try:
    db_service = DatabaseService(
        host=Config.POSTGRES_HOST,
        port=Config.POSTGRES_PORT,
        database=Config.POSTGRES_DB,
        user=Config.POSTGRES_USER,
        password=Config.POSTGRES_PASSWORD
    )
    logger.info("Database service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize database service: {e}")
    logger.warning("History tracking will be unavailable")

# Initialize history service
if db_service:
    history_service = HistoryService(db_service)
    init_history_routes(history_service)
    app.register_blueprint(history_bp)
    logger.info("History routes registered successfully")

# Register existing blueprints
app.register_blueprint(words_bp, url_prefix='/api/words')
app.register_blueprint(health_bp)

# Cleanup on shutdown
def cleanup():
    if db_service:
        db_service.close_all()
        logger.info("Application shutdown: database connections closed")

atexit.register(cleanup)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
