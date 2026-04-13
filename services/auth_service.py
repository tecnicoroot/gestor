from database.repositories.user_repository import UserRepository
from utils.security import verify_password

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def login(self, username, password):
        user = self.repo.find_by_username(username)

        if not user:
            return None

        user_id, usr, hashed, role = user

        if verify_password(password, hashed):
            return {
                "id": user_id,
                "username": usr,
                "role": role
            }

        return None