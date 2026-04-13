from database.repositories.user_repository import UserRepository
from utils.security import hash_password

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    # =========================
    # CREATE
    # =========================
    def create_user(self, username, password, role="user"):
        if not username or not password:
            raise ValueError("Usuário e senha são obrigatórios")

        if self.repo.get_by_username(username):
            raise ValueError("Usuário já existe")


        return self.repo.create(
            username,
            hash_password(password),
            role
        )

    # =========================
    # READ (ALL)
    # =========================
    def get_all(self):
        return self.repo.get_all()

    # =========================
    # READ (BY ID)
    # =========================
    def get_by_id(self, user_id):
        return self.repo.get_by_id(user_id)

    # =========================
    # UPDATE
    # =========================
    def update_user(self, user_id, username, password, role):
        if not username:
            raise ValueError("Usuário é obrigatório")

        data = {
            "username": username,
            "role": role
        }

        # só atualiza senha se foi informada
        if password:
            data["password"] = hash_password(password)

        return self.repo.update(user_id, data)

    # =========================
    # DELETE
    # =========================
    def delete_user(self, user_id, current_user_id=None):
        if not user_id:
            raise ValueError("ID inválido")
        
        if user_id == current_user_id:
            raise ValueError("Você não pode deletar seu próprio usuário")

        return self.repo.delete(user_id)