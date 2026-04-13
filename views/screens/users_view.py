import bcrypt
import customtkinter as ctk
from controllers.user_controller import UserController
from models.models import User
class UsersView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container

        self.controller = UserController(self, container)

        # 🌑 fundo padrão ERP
        self.configure(fg_color="#0f172a")

        self.status_display_to_db = {
            "Ativo": "ACTIVE",
            "Inativo": "INACTIVE",
            "Suspenso": "SUSPENDED"
        }
        self.status_db_to_display = {v: k for k, v in self.status_display_to_db.items()}
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
        # CAMPOS DE ENTRADA (lado a lado)
        # =========================
        entries_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        entries_frame.pack(pady=10)

        # Primeira linha: Nome | E-mail
        self.name = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Nome",
            width=300,
            height=40,
            corner_radius=10
        )
        self.name.grid(row=0, column=0, padx=5, pady=5)

        self.email = ctk.CTkEntry(
            entries_frame,
            placeholder_text="E-mail",
            width=300,
            height=40,
            corner_radius=10
        )
        self.email.grid(row=0, column=1, padx=5, pady=5)

        # Segunda linha: Usuário | Senha
        self.username = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Usuário",
            width=300,
            height=40,
            corner_radius=10
        )
        self.username.grid(row=1, column=0, padx=5, pady=5)

        self.password = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Senha",
            show="*",
            width=300,
            height=40,
            corner_radius=10
        )
        self.password.grid(row=1, column=1, padx=5, pady=5)

        # Status abaixo dos campos (centralizado)
        self.add_status_entry = ctk.CTkComboBox(
            entries_frame,
            width=300,
            height=40,
            corner_radius=10,
            values=["Ativo", "Inativo", "Suspenso"]
        )
        self.add_status_entry.grid(row=2, column=0, padx=5, pady=5)

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

        self.list_frame.configure(width=1024, height=400)
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
        user = self.get_user_from_inputs()
        if hasattr(self, "editing_user_id"):
            user.id = self.editing_user_id
            # Se o campo senha estiver vazio, mantenha a antiga
            if not user.password:
                user_old = self.controller.get_by_id(user.id)
                user.password = user_old.password
            self.controller.update_user(user)
            del self.editing_user_id
        else:
            self.controller.create_user(user)

        self.limpa_inputs()
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
            text=user.id,
            text_color="white",
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            row,
            text=user.username,
            text_color="white",
            width=150,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            row,
            text=user.email,
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

    def get_user_from_inputs(self):
        # Converte o valor do combo para o valor aceito pelo banco
        status_display = self.add_status_entry.get()
        status_db = self.status_display_to_db.get(status_display, "ACTIVE")
        return User(
            name=self.name.get(),
            email=self.email.get(),
            username=self.username.get(),
            password=self.password.get(),
            status=status_db
        )

    def limpa_inputs(self):
        self.name.delete(0, "end")
        self.email.delete(0, "end")
        self.username.delete(0, "end")
        self.password.delete(0, "end")
        self.add_status_entry.set("")

    def delete_user(self, user):
        self.controller.delete_user(user.id)
        self.load_users()

    def edit_user(self, user):
        self.limpa_inputs()

        self.username.insert(0, user.username)
        self.name.insert(0, user.name)
        self.email.insert(0, user.email)
        self.password.insert(0, "")
        status_db = user.status
        status_db_key = status_db.name if hasattr(status_db, "name") else str(status_db)
        status_display = self.status_db_to_display.get(status_db_key, "Ativo")
        self.add_status_entry.set(status_display)

        self.editing_user_id = user.id