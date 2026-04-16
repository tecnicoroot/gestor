from core.state import AppState


class LoginController:
    def __init__(self, view, router, container):
        self.view = view
        self.router = router
        self.container = container


    def login(self, username, password):
        user = self.container.auth_service.login(username, password)

        if user:
            print("✅ Login OK")
            self.container.state.clear()
            self.container.state.user = user

            # ❌ NÃO FECHAR JANELA
            # self.app.destroy()  ← PROIBIDO
            # Alimenta o AppState
            self.container.state.user = user["user"]
            self.container.state.roles = user["roles"]
            self.container.state.claims = {c['value']: True for c in user["claims"]}

            #print(vars(self.app_state.user))
            self.router.navigate("dashboard")
        else:
            self.view.show_error("Login inválido")
    def logout(self):
        self.container.state.clear()
        self.router.navigate("login")