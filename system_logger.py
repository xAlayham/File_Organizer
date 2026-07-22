import logging, os

def setup_logger():
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        filename=os.path.join("logs", "app.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

def log_execution(result):
    if result['failed'] == 0:
        logging.info("Execution completed successfully")
    else:
        logging.warning("Execution completed with errors")

def info(msg):
    logging.info(msg)

def warning(msg):
    logging.warning(msg)

def error(msg):
    logging.error(msg)

def debug(msg):
    logging.debug(msg)