import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'message': record.getMessage()
        }
        if hasattr(record, 'extra_data'):
            log_record['extra'] = record.extra_data
        return json.dumps(log_record)

def setup_logging():
    logger = logging.getLogger('api_logger')
    logger.setLevel(logging.INFO)

    file_handler = RotatingFileHandler(
        'app.log',
        maxBytes = 5_000_000,
        backupCount = 3

    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(JSONFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(JSONFormatter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.propagate = False
    return logger
