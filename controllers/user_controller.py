class UserController:
    def __init__(self, view, container):
        self.view = view
        self.service = container.user_service

    def create_user(self, user):
        try:
            self.service.create_user(user.username, user.password, user.name, user.email)
            self.view.show_success("Usuário criado com sucesso!")
        except Exception as e:
            self.view.show_error(str(e))
    
    def get_all_users(self):
        return self.service.get_all()

    def get_by_id(self, id):
        return self.service.get_by_id(id)

    def delete_user(self, user_id):
        self.service.delete_user(user_id)

    def update_user(self, user ):
        self.service.update_user(user)