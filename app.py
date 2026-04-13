import customtkinter as ctk
from core.router import Router
from core.container import Container
from database.connection import SessionLocal

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ERP Sistema")

        # FULLSCREEN REAL
        self.attributes("-fullscreen", True)

        # sair do fullscreen com ESC
        self.bind("<Escape>", self.exit_fullscreen)

        self.container = Container()
        self.router = Router(self, self.container)

        self.router.navigate("login") 

    def exit_fullscreen(self, event=None):
        self.attributes("-fullscreen", False)

    # 🔥 método de fechamento seguro
    def exit_app(self, event=None):
        self.destroy()