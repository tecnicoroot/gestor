class UserController:
    def __init__(self, view, container):
        self.view = view
        self.service = container.user_service

    def create_user(self, username, password, role):
        try:
            self.service.create_user(username, password, role)
            self.view.show_success("Usuário criado com sucesso!")
        except Exception as e:
            self.view.show_error(str(e))
    
    def get_all_users(self):
        return self.service.get_all()

    def delete_user(self, user_id):
        self.service.udelete(user_id)

    def update_user(self, user_id, username, password, role):
        self.service.update(user_id, username, password, role)