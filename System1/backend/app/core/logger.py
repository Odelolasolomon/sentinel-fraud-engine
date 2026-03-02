import sys
from loguru import logger

def setup_logging():
    # Production Logging: JSON format for ELK/CloudWatch consumption
    logger.remove()
    logger.add(
        sys.stdout, 
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", 
        level="INFO",
        backtrace=True,
        diagnose=False
    )
    logger.add("logs/fraud_engine.log", rotation="500 MB", retention="10 days", level="DEBUG")

setup_logging()
