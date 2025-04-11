import logging 
import os 
import datetime

"""
Create a log file in the logs directory with the current date.
Appends in the log file if it already exists.
Each day a new log file is created and the logs are appended to it.
It is used to log the information and the errors of the car and the sensors.
The format of the message is : 
    Date and time - Level - Message
"""

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_path = os.path.join(
        log_dir,
        f"LamboCar_{datetime.datetime.now().date()}.log"
    )
    
    logging.basicConfig(
        filename=log_path,
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.INFO,
        filemode='a'
    )
