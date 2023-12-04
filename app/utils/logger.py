import os
import logging

os.makedirs('logs', exist_ok=True)

# Create a logger for general application logging
app_logger = logging.getLogger('app')
app_logger.setLevel(logging.INFO)
handler = logging.FileHandler('logs/app.log')
handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)-8s %(message)s'))
app_logger.addHandler(handler)


# Create a logger for HTTP request scenarios
http_logger = logging.getLogger('http_requests')
http_logger.setLevel(logging.ERROR)
http_handler = logging.FileHandler('logs/http_requests.log')
http_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s'))
http_logger.addHandler(http_handler)
