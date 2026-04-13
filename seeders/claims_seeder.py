

import bcrypt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import sessionmaker
from models.models import Status, Claim
from database.connection import SessionLocal  # supondo que você tem um `engine`

def seed_claims():
    session = SessionLocal()
    #log = Logger(name='AppLogger', log_file='app.log', level=logging.DEBUG)

    try:
        claims = ["create_user", "read_user", "update_user",  "delete_user",
                  "create_claim", "read_claim", "update_claim",  "delete_claim",
                  "create_role", "read_role", "update_role",  "delete_role",
                  "create_outros",  "read_outros","update_outros", "delete_outros"]

        for c in claims:

            if not session.query(Claim).filter_by(value=c).first():
                claim = Claim(
                    value=c,
                    type="permission"

                )
                # print(user_admin.password)
                session.add(claim)
                print(f"Claim {c} criado.")
                # log.info("Usuário admin criado.")
            else:
                print(f"Claim {c} já está cadastrada.")
                # log.error("Usuário admin já existe.")

            session.commit()
    except Exception as e:
        session.rollback()
        print(f"Erro ao executar seeder: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    seed_claims()