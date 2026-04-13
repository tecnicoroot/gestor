import logging

from logs.handler_db import LogAccessHandler
from models.dao.log_access_dao import LogAccessDao
from database.db import SessionLocal, engine

class Logger:
    def __init__(self, name='AppLogger', log_file='app.log', level=logging.DEBUG, user_id=0):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False

        if not self.logger.handlers:
            # File handler
            file_handler = logging.FileHandler(log_file)
            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(filename)s - Linha: %(lineno)d - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)

            # Database handler
            db_handler = LogAccessHandler(SessionLocal, user_id=user_id)
            db_formatter = logging.Formatter('%(name)s - %(filename)s - %(lineno)d - %(message)s')
            db_handler.setFormatter(db_formatter)
            self.logger.addHandler(db_handler)

            # Optional: Console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(file_formatter)
            self.logger.addHandler(console_handler)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def critical(self, msg):
        self.logger.critical(msg)

    def exception(self, msg):
        self.logger.exception(msg)

if __name__ == "__main__":
    log = Logger()

    log.info("teste")