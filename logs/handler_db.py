import logging
from datetime import datetime
from models.models import LogAccess

class LogAccessHandler(logging.Handler):
    def __init__(self, SessionLocal, user_id=None):
        super().__init__()
        self.SessionLocal = SessionLocal
        self.user_id = user_id  # opcional: logar com base no usuário atual

    def emit(self, record):
        session = self.SessionLocal()
        try:
            log_entry = LogAccess(
                user_id=self.user_id,  # pode ser None
                level=record.levelname,
                message=self.format(record),
                created_at=datetime.utcnow()  # redundante, mas explícito
            )
            session.add(log_entry)
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"[LogAccessHandler] Erro ao salvar log no banco: {e}")
        finally:
            session.close()
