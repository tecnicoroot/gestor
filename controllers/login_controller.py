from core.state import AppState


class LoginController:
    def __init__(self, view, router, container):
        self.view = view
        self.router = router
        self.container = container
        self.app_state = AppState()

    def login(self, username, password):
        user = self.container.auth_service.login(username, password)

        if user:
            print("✅ Login OK")

            self.container.state.user = user

            # ❌ NÃO FECHAR JANELA
            # self.app.destroy()  ← PROIBIDO
            # Alimenta o AppState
            self.app_state.user = user["user"]
            self.app_state.roles = user["roles"]
            self.app_state.claims = user["claims"]

            #print(vars(self.app_state.user))
            self.router.navigate("dashboard")
        else:
            self.view.show_error("Login inválido")