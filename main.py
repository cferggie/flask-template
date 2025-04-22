from server import create_app
from utils.logger import setup_logger
import os

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Get logger and add handler
app = create_app()
logger = setup_logger(__name__)

if __name__ == '__main__':
    logger.info("Starting Flask server on port 5000")
    app.run(debug=True, port=5000, host='0.0.0.0') 