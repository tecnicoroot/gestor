class AppState:
    def __init__(self):
        self.user = None

    def is_admin(self):
        return self.user and self.user["role"] == "admin"