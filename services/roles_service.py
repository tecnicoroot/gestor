from database.repositories.roles_repository import RoleRepository
from database.repositories.claims_repository import ClaimRepository

class RoleService:
    def __init__(self):
        self.repo = RoleRepository()
        self.repo_claims = ClaimRepository()

    # =========================
    # CREATE
    # =========================
    def create_role(self, role):
        if not role.name:
            raise ValueError("Nome é obrigatório")

        return self.repo.create(
            role
        )

    # =========================
    # READ (ALL)
    # =========================
    def get_all_role(self):
        return self.repo.get_all_role()

    def get_all_claim(self):
        return self.repo.get_all_claim()
    # =========================
    # READ (BY ID)
    # =========================
    def get_by_id(self, role_id):
        return self.repo.find_by_id(role_id)

    # =========================
    # UPDATE
    # =========================
    def update_role(self, role):
        if not role.name:
            raise ValueError("Usuário é obrigatório")

        return self.repo.update(role)

    # =========================
    # DELETE
    # =========================
    def delete_role(self, role_id, current_role_id=None):
        if not role_id:
            raise ValueError("ID inválido")

        if role_id == current_role_id:
            raise ValueError("Você não pode deletar seu próprio usuário")

        return self.repo.delete(role_id)

    def set_claims_for_role(self, role_id, claim_ids):
        return self.repo.set_claims_for_role(role_id, claim_ids)