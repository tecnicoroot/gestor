class LoginController:
    def __init__(self, view, router, container):
        self.view = view
        self.router = router
        self.container = container

    def login(self, username, password):
        user = self.container.auth_service.login(username, password)

        if user:
            print("✅ Login OK")

            self.container.state.user = user

            # ❌ NÃO FECHAR JANELA
            # self.app.destroy()  ← PROIBIDO

            self.router.navigate("dashboard")
        else:
            self.view.show_error("Login inválido")