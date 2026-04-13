from database.repositories.user_repository import UserRepository
from utils.security import hash_password

class UserService:
    def __init__(self):
        self.repo = UserRepository()

    # =========================
    # CREATE
    # =========================
    def create_user(self, user):
        if not user.username or not user.password:
            raise ValueError("Usuário e senha são obrigatórios")

        if self.repo.find_by_username(user.username):
            raise ValueError("Usuário já existe")


        return self.repo.create(
            user
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
        return self.repo.find_by_id(user_id)

    # =========================
    # UPDATE
    # =========================
    def update_user(self, user):
        if not user.username:
            raise ValueError("Usuário é obrigatório")

        # só atualiza senha se foi informada
        if  user.password:

            user.password = hash_password(user.password)

        return self.repo.update(user)

    # =========================
    # DELETE
    # =========================
    def delete_user(self, user_id, current_user_id=None):
        if not user_id:
            raise ValueError("ID inválido")
        
        if user_id == current_user_id:
            raise ValueError("Você não pode deletar seu próprio usuário")

        return self.repo.delete(user_id)