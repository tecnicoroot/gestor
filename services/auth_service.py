import bcrypt

from database.repositories.user_repository import UserRepository
from utils.security import verify_password

class AuthService:
    def __init__(self):
        self.repo = UserRepository()

    def login(self, username, password):
        user = self.repo.find_by_username(username)

        if not user:
            return None

        #user_id, usr, hashed, role = user

        if bcrypt.checkpw(password.encode(), user.password):
            # Monta roles (nomes)
            roles = [role.name for role in user.roles]

            # Monta claims (type: value)
            claims = []
            for role in user.roles:
                for claim in role.claims:
                    claims.append({"type": claim.type, "value": claim.value, "role": role.name})

            # Retorna um dicionário/dto pronto para alimentar o AppState
            return {
                "user": user,
                "roles": roles,
                "claims": claims
            }

        return None