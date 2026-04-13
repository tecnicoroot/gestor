class Router:
    def __init__(self, app, container):
        self.app = app
        self.container = container
        self.frames = {}

        self.routes = {
            "login": lambda: __import__("views.screens.login_view", fromlist=["LoginView"]).LoginView,
            "dashboard": lambda: __import__("views.screens.dashboard_view", fromlist=["DashboardView"]).DashboardView,
            "users": lambda: __import__("views.screens.users_view", fromlist=["UsersView"]).UsersView,
        }

    def navigate(self, route):
        print(f"🔁 Navegando para: {route}")

        # cria só uma vez
        if route not in self.frames:
            frame_class = self.routes[route]()
            frame = frame_class(self.app, self, self.container)

            self.frames[route] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

        # troca visibilidade (SEM destruir)
        self.frames[route].tkraise()

        # opcional lifecycle hook
        frame = self.frames[route]
        if hasattr(frame, "on_show"):
            frame.on_show()