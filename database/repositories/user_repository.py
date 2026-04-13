from database.connection import SessionLocal
from models.models import User

class UserRepository:
    # Cria um novo usuário a partir de uma instância de User
    def create(self, user: User):
        session = SessionLocal()
        session.add(user)
        session.commit()
        session.refresh(user)  # Para garantir ID atualizado etc.
        session.close()
        return user

    # Busca e retorna User pelo username
    def find_by_username(self, username: str) -> User | None:
        session = SessionLocal()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user

    # Busca e retorna User pelo id
    def find_by_id(self, id: int) -> User | None:
        session = SessionLocal()
        user = session.query(User).filter_by(id=id).first()
        session.close()
        return user

    # Retorna todos os usuários como lista de User
    def get_all(self) -> list[User]:
        session = SessionLocal()
        users = session.query(User).all()
        session.close()
        return users

    # Deleta um usuário a partir de um objeto User
    def delete(self, user: User):
        session = SessionLocal()
        user_db = session.query(User).filter_by(id=user.id).first()
        if user_db:
            session.delete(user_db)
            session.commit()
        session.close()

    # Atualiza um usuário a partir de uma instância de User (id deve existir)
    def update(self, user: User):
        session = SessionLocal()
        user_db = session.query(User).filter_by(id=user.id).first()
        if not user_db:
            session.close()
            return None

        # Atualize campos individualmente, exceto o id
        user_db.username = user.username
        user_db.password = user.password
        user_db.name = user.name
        user_db.email = user.email
        user_db.status = user.status

        session.commit()
        session.refresh(user_db)
        session.close()
        return user_db