from database.connection import SessionLocal
from models.models import User, Role
from sqlalchemy.orm import joinedload
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
        user = session.query(User)\
            .options(
                joinedload(User.roles).joinedload(Role.claims)
            )\
            .filter_by(username=username).first()
        session.close()
        return user

    # Busca e retorna User pelo id
    def find_by_id(self, id: int) -> User | None:
        session = SessionLocal()
        user = session.query(User).filter_by(id=id).first()
        session.close()
        return user

    # Retorna todos os usuários como lista de User
    def get_all_user(self) -> list[User]:
        with SessionLocal() as session:
            return session.query(User).all()

    def get_all_roles(self) -> list[Role]:
        with SessionLocal() as session:
            return session.query(Role).all()

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

    def set_roles_for_user(self, user_id, role_ids):
        with SessionLocal() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return False

            roles = session.query(Role).filter(Role.id.in_(role_ids)).all()
            user.roles = roles
            session.commit()
            return True

    def get_roles_by_user(self, user_id):
        with SessionLocal() as session:
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return []

            return user.roles