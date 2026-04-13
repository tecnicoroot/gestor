import customtkinter as ctk
from controllers.login_controller import LoginController
from tkinter import messagebox

class LoginView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container
        self.controller = LoginController(self, router, container)

        # 🌑 fundo geral
        self.configure(fg_color="#0f172a")

        # =========================
        # 🧊 CARD CENTRAL
        # =========================
        self.card = ctk.CTkFrame(
            self,
            width=350,
            height=400,
            corner_radius=20,
            fg_color="#0f172a"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")

        # =========================
        # TÍTULO
        # =========================
        ctk.CTkLabel(
            self.card,
            text="ERP LOGIN",
            font=("Ariall", 24, "bold"),
            text_color="white"
        ).pack(pady=30)

        # =========================
        # INPUT USER
        # =========================
        self.username = ctk.CTkEntry(
            self.card,
            placeholder_text="Usuário",
            width=250,
            height=40,
            corner_radius=10
        )
        self.username.pack(pady=10)

        # =========================
        # INPUT PASSWORD
        # =========================
        self.password = ctk.CTkEntry(
            self.card,
            placeholder_text="Senha",
            show="*",
            width=250,
            height=40,
            corner_radius=10
        )
        self.password.pack(pady=10)

        # =========================
        # BOTÃO LOGIN
        # =========================
        ctk.CTkButton(
            self.card,
            text="ENTRAR",
            width=250,
            height=45,
            corner_radius=10,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=("Ariall", 14, "bold"),
            command=self.on_login
        ).pack(pady=20)

        # =========================
        # BOTÃO SAIR
        # =========================
        ctk.CTkButton(
            self.card,
            text="SAIR",
            width=250,
            height=40,
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=self.app.destroy
        ).pack(pady=5)

        # =========================
        # FOOTER
        # =========================
        ctk.CTkLabel(
            self.card,
            text="Sistema ERP • v1.0",
            text_color="#94a3b8",
            font=("Ariall", 10)
        ).pack(pady=10)
        
        self.username.bind("<Return>", lambda e: self.password.focus())
        self.password.bind("<Return>", lambda e: self.on_login())


    def on_login(self):
        self.controller.login(
            self.username.get(),
            self.password.get()
        )

    def show_error(self, msg):
        messagebox.showerror("Erro", msg)