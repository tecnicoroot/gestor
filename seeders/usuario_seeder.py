

import bcrypt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from models.models import Status, User
from database.connection import SessionLocal  # supondo que você tem um `engine`

def seed_usuarios():
    session = SessionLocal()
    #log = Logger(name='AppLogger', log_file='app.log', level=logging.DEBUG)

    try:
        if not session.query(User).filter_by(username="admin").first():
            user_admin = User(
                name="Administrador",
                email="administrador@sistena.com",
                username="admin",
                password=bcrypt.hashpw(b"123", bcrypt.gensalt()),
                status=Status.ACTIVE
            )
            #print(user_admin.password)
            session.add(user_admin)
            print("Usuário admin criado.")
            #log.info("Usuário admin criado.")
        else:
            print("Usuário admin já existe.")
            #log.error("Usuário admin já existe.")

        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao executar seeder: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_usuarios()