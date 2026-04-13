
class RolesController:
    def __init__(self, view, container):
        self.view = view
        self.service = container.role_service

    def create_role(self, role):
        try:
            self.service.create_role(role)
            self.view.show_success("Perfil criado com sucesso!")
        except Exception as e:
            self.view.show_error(str(e))

    def get_all_roles(self):
        return self.service.get_all_role()

    def get_by_id(self, id):
        return self.service.get_by_id(id)

    def delete_role(self, role_id):
        self.service.delete_role(role_id)

    def update_role(self, role):
        self.service.update_role(role)

    def get_all_claims(self):
        return self.service.get_all_claim()

    def set_claims_for_role(self, role_id, claim_ids):
        return self.service.set_claims_for_role(role_id, claim_ids)
    
    def get_claims_by_role(self, role_id):
        return self.service.get_claims_by_role(role_id)