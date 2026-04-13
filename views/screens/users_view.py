import customtkinter as ctk
from controllers.user_controller import UserController

class UsersView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container

        self.controller = UserController(self, container)

        # 🌑 fundo padrão ERP
        self.configure(fg_color="#0f172a")
        

        # =========================
        # 🧱 CONTAINER PRINCIPAL
        # =========================
        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=15
        )
        self.main_frame.place(relx=0.5, rely=0.3, anchor="center")

        self.main_frame.configure(width=800, height=400)
        self.main_frame.pack_propagate(False)

        # =========================
        # 📋 TÍTULO
        # =========================
        ctk.CTkLabel(
            self.main_frame,
            text="👤 Cadastro de Usuários",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=20)

        # =========================
        # INPUT USERNAME
        # =========================
        self.username = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Usuário",
            width=300,
            height=40,
            corner_radius=10
        )
        self.username.pack(pady=10)

        # =========================
        # INPUT PASSWORD
        # =========================
        self.password = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Senha",
            show="*",
            width=300,
            height=40,
            corner_radius=10
        )
        self.password.pack(pady=10)

        # =========================
        # ROLE SELECT
        # =========================
        self.role = ctk.CTkOptionMenu(
            self.main_frame,
            values=["user", "admin"],
            width=300
        )
        self.role.pack(pady=10)

        # =========================
        # BOTÕES
        # =========================
        ctk.CTkButton(
            self.main_frame,
            text="💾 Salvar Usuário",
            width=300,
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.save_user
        ).pack(pady=15)

        ctk.CTkButton(
            self.main_frame,
            text="⬅ Voltar",
            width=300,
            height=35,
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: self.router.navigate("dashboard")
        ).pack(pady=5)

        # =========================
        # FEEDBACK
        # =========================
        self.message_label = ctk.CTkLabel(
            self.main_frame,
            text="",
            text_color="#94a3b8"
        )
        self.message_label.pack(pady=10)

        # =========================
        # 📋 LISTA DE USUÁRIOS
        # =========================
        self.list_frame = ctk.CTkFrame(
            self,
            fg_color="#0f172a"
        )
        self.list_frame.place(relx=0.5, rely=0.75, anchor="center")

        self.list_frame.configure(width=800, height=400)
        self.list_frame.pack_propagate(False)

        self.users_container = ctk.CTkScrollableFrame(
            self.list_frame,
            fg_color="transparent"
        )
        self.users_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_users()
    # =========================
    # SALVAR USUÁRIO
    # =========================
    def save_user(self):
        if hasattr(self, "editing_user_id"):
            self.controller.update_user(
                self.editing_user_id,
                self.username.get(),
                self.password.get(),
                self.role.get()
            )
            del self.editing_user_id
        else:
            self.controller.create_user(
                self.username.get(),
                self.password.get(),
                self.role.get()
            )

        self.username.delete(0, "end")
        self.password.delete(0, "end")

        self.load_users()

    # =========================
    # FEEDBACK UI
    # =========================
    def show_success(self, msg):
        self.message_label.configure(text=msg, text_color="#22c55e")

    def show_error(self, msg):
        self.message_label.configure(text=msg, text_color="#ef4444")

    def destroy(self):
        try:
            self.username.unbind("<Return>")
            self.password.unbind("<Return>")
        except:
            pass
        super().destroy()

    def load_users(self):
        # limpa lista
        for widget in self.users_container.winfo_children():
            widget.destroy()

        users = self.controller.get_all_users()

        for user in users:
            self.add_user_row(user)
    
    def add_user_row(self, user):
        row = ctk.CTkFrame(self.users_container, fg_color="#1e293b")
        row.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(
            row,
            text=user["id"],
            text_color="white",
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            row,
            text=user["username"],
            text_color="white",
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            row,
            text=user["role"],
            text_color="#94a3b8",
            width=100
        ).pack(side="left")

        # ✏️ EDITAR
        ctk.CTkButton(
            row,
            text="Editar",
            width=80,
            fg_color="#eab308",
            hover_color="#ca8a04",
            command=lambda u=user: self.edit_user(u)
        ).pack(side="right", padx=5)

        # 🗑️ DELETAR
        ctk.CTkButton(
            row,
            text="Excluir",
            width=80,
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=lambda u=user: self.delete_user(u)
        ).pack(side="right", padx=5)
    
    def delete_user(self, user):
        self.controller.delete_user(user["id"])
        self.load_users()
    
    def edit_user(self, user):
        self.username.delete(0, "end")
        self.password.delete(0, "end")

        self.username.insert(0, user["username"])
        self.role.set(user["role"])

        self.editing_user_id = user["id"]