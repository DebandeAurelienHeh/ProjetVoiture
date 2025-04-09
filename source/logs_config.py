import logging 

def setup_logging():
    logging.basicConfig(
        filename="LamboCar_warnings_errors.log",
        format='%(asctime)s - %(levelname)s - %(message)s',
        level=logging.WARNING,
        filemode='a')