import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container

        # 🌑 fundo geral (mesmo do login)
        self.configure(fg_color="#0f172a")

        # =========================
        # 📋 SIDEBAR (MENU)
        # =========================
        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            fg_color="#1e293b",
            corner_radius=0
        )
        self.sidebar.pack(side="left", fill="y")

        user = self.container.state.user

        ctk.CTkLabel(
            self.sidebar,
            text="ERP SYSTEM",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=20)

        ctk.CTkLabel(
            self.sidebar,
            text=f"{user['username']}",
            text_color="#94a3b8",
            font=("Arial", 12)
        ).pack(pady=5)

        ctk.CTkLabel(
            self.sidebar,
            text=f"Role: ",
            text_color="#64748b",
            font=("Arial", 10)
        ).pack(pady=5)

        # =========================
        # BOTÕES MENU
        # =========================
        ctk.CTkButton(
            self.sidebar,
            text="Dashboard",
            fg_color="transparent",
            text_color="white",
            hover_color="#334155",
            anchor="w",
            command=self.show_home
        ).pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(
            self.sidebar,
            text="Usuários",
            fg_color="transparent",
            text_color="white",
            hover_color="#334155",
            anchor="w",
            command=lambda: self.router.navigate("users")
        ).pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(
            self.sidebar,
            text="Perfis",
            fg_color="transparent",
            text_color="white",
            hover_color="#334155",
            anchor="w",
            command=lambda: self.router.navigate("perfis")
        ).pack(fill="x", pady=5, padx=10)

        ctk.CTkButton(
            self.sidebar,
            text="🚪 Sair",
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=self.logout
        ).pack(side="bottom", fill="x", padx=10, pady=20)

        # =========================
        # 📦 CONTEÚDO PRINCIPAL
        # =========================
        self.content = ctk.CTkFrame(
            self,
            fg_color="#0f172a"
        )
        self.content.pack(side="left", fill="both", expand=True)

        self.show_home()

    # =========================
    # HOME DASHBOARD
    # =========================
    def show_home(self):
        self.clear()

        ctk.CTkLabel(
            self.content,
            text="Dashboard",
            font=("Arial", 26, "bold"),
            text_color="white"
        ).pack(pady=30)

        # 📊 CARDS
        card_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        card_frame.pack(pady=20)

        self.create_card(card_frame, "Usuários", "12")
        self.create_card(card_frame, "Vendas", "R$ 8.500")
        self.create_card(card_frame, "Produtos", "34")

    # =========================
    # CARD COMPONENT
    # =========================
    def create_card(self, parent, title, value):
        card = ctk.CTkFrame(
            parent,
            width=180,
            height=120,
            fg_color="#1e293b",
            corner_radius=15
        )
        card.pack(side="left", padx=10)

        ctk.CTkLabel(
            card,
            text=title,
            text_color="#94a3b8",
            font=("Arial", 12)
        ).pack(pady=10)

        ctk.CTkLabel(
            card,
            text=value,
            text_color="white",
            font=("Arial", 20, "bold")
        ).pack()

    # =========================
    # LIMPAR CONTEÚDO
    # =========================
    def clear(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # =========================
    # LOGOUT
    # =========================
    def logout(self):
        self.container.state.user = None
        self.router.navigate("login")