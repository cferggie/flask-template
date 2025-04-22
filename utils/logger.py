import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    """
    Creates and configures a logger instance.
    
    Args:
        name (str): The name of the logger (typically __name__ from the calling module)
        
    Returns:
        logging.Logger: Configured logger instance
    """
    # Get the filename from the logger name and create its directory
    filename = name.split('.')[-1]  # Gets the last part of the module path
    if filename != '__main__':
        log_dir = os.path.join('logs', filename)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    else:
        log_dir = 'logs'
        
    # Create logger
    logger = logging.getLogger(name)
    
    # Only add handlers if the logger doesn't already have them
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(
            filename=os.path.join(log_dir, f'{datetime.now().strftime("%Y-%m-%d")}.log'),
            mode='a'
        )
        
        # Set levels
        console_handler.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        
        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            '%(asctime)s - %(filename)s - %(levelname)s - %(funcName)s - %(message)s'
        )
        console_handler.setFormatter(log_format)
        file_handler.setFormatter(log_format)
        
        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    
    return logger