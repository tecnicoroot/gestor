from sys import maxsize

import bcrypt
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
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
        # FRAME DE DUAS COLUNAS
        self.columns_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.columns_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # =========================
        # 📦 COLUNA 1: CADASTRO E LISTA DE ROLES
        # =========================
        self.left_frame = ctk.CTkFrame(self.columns_frame, fg_color="#0f172a", corner_radius=15)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        self.columns_frame.grid_columnconfigure(0, weight=5)
        self.columns_frame.grid_columnconfigure(1, weight=1)
        # =========================
        # 🧱 CONTAINER PRINCIPAL
        # =========================
        self.main_frame = ctk.CTkFrame(
            self.left_frame,
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
            self.left_frame,
            text="Cadastro de Usuários",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=20)

        # =========================
        # CAMPOS DE ENTRADA (lado a lado)
        # =========================
        entries_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
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
            self.left_frame,
            text="Salvar Usuário",
            width=300,
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.save_user
        ).pack(pady=15)

        ctk.CTkButton(
            self.left_frame,
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
            self.left_frame,
            text="",
            text_color="#94a3b8"
        )
        self.message_label.pack(pady=10)

        # =========================
        # 📋 LISTA DE USUÁRIOS
        # =========================
        #self.list_frame = ctk.CTkFrame(
        #    self.left_frame,
        #    fg_color="#0f172a"
        #)
        #self.list_frame.place(relx=0.5, rely=0.75, anchor="center")

        ##self.left_frame.configure(width=1024, height=400)
        ##self.list_frame.pack_propagate(False)

        ##self.users_container = ctk.CTkScrollableFrame(
        ##    self.list_frame,
        ##    fg_color="transparent"
        #)
        #self.users_container.pack(fill="both", expand=True, padx=10, pady=10)

        self.user_container = ctk.CTkScrollableFrame(self.left_frame, fg_color="#1e293b", height=320)
        self.user_container.pack(fill="x", expand=False, padx=5, pady=5)

        # =========================
        # 📦 COLUNA 2: roles
        # =========================
        self.right_frame = ctk.CTkFrame(self.columns_frame, fg_color="#fff9c4")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)
        self.right_frame.grid_propagate(False)
        self.right_frame.configure(width=100)
        ctk.CTkLabel(self.right_frame, text="Acessos Disponíveis",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(12, 4), anchor="center")

        self.labels_frame = ctk.CTkFrame(self.right_frame, fg_color="#fff9c4")
        self.labels_frame.pack(pady=(0, 8), anchor="w")
        ctk.CTkFrame(self.right_frame, height=2, fg_color="#aee1ab").pack(fill="x", padx=5, pady=5)
        label_width = 120
        for label_text in ["Perfis"]:
            ctk.CTkLabel(self.labels_frame, text=label_text, font=ctk.CTkFont(size=14, weight="bold"),
                         width=label_width, anchor="center").pack(side="left", padx=0)

        self.roles_outer_frame = ctk.CTkFrame(self.right_frame, fg_color="#fff9c4")
        self.roles_outer_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.roles_canvas = tk.Canvas(self.roles_outer_frame, bg="#fff9c4", highlightthickness=0)
        self.roles_canvas.pack(side="left", fill="both", expand=True)
        self.roles_scrollbar = tk.Scrollbar(self.roles_outer_frame, orient="vertical",
                                             command=self.roles_canvas.yview)
        self.roles_scrollbar.pack(side="right", fill="y")
        self.roles_canvas.configure(yscrollcommand=self.roles_scrollbar.set)
        self.roles_grid = ctk.CTkFrame(self.roles_canvas, fg_color="#fff9c4")
        self.roles_canvas.create_window((0, 0), window=self.roles_grid, anchor="nw")

        ctk.CTkButton(self.right_frame, text="Salvar Permissões", command=self.save_roles).pack(pady=12)

        # --- DADOS INTERNOS ---
        self.users = []
        self.roles = []
        self.roles_vars = {}
        self.roles_widgets = {}
        self.selected_user_id = None

        self.load_roles()
        self.load_users()

    # =========================
    # SALVAR USUÁRIO
    # =========================
    def save_user(self):
        user = self.get_user_from_inputs()
        if hasattr(self, "editing_user_id"):
            print("edit")
            user.id = self.editing_user_id
            # Se o campo senha estiver vazio, mantenha a antiga
            if not user.password:
                user_old = self.controller.get_by_id(user.id)
                user.password = user_old.password
            self.controller.update_user(user)
            del self.editing_user_id
        else:
            print("create")
            self.controller.create_user(user)
        self.limpa_inputs()
        self.load_users()
    
    def load_roles(self):
        # Limpa checkboxes antigos
        for widget in self.roles_grid.winfo_children():
            widget.destroy()
        self.roles = self.controller.get_all_roles()
        self.roles_vars.clear()
        self.roles_widgets.clear()
        columns = 1
        checkboxes_per_group = 1

        columns_roles = [[] for _ in range(columns)]
        for idx, role in enumerate(self.roles):
            col = idx % columns
            columns_roles[col].append(role)
        max_column_length = max(len(col_roles) for col_roles in columns_roles) if columns_roles else 0
        row_counter = 1

        for row in range(max_column_length):
            for col in range(columns):
                if row < len(columns_roles[col]):
                    role = columns_roles[col][row]
                    var = ctk.BooleanVar()
                    cb = ctk.CTkCheckBox(self.roles_grid, text=f"{role.name}", variable=var)
                    cb.grid(row=row_counter, column=col, sticky="w", padx=6, pady=2)
                    self.roles_vars[role.id] = var
                    self.roles_widgets[role.id] = cb
            row_counter += 1

        self.roles_grid.update_idletasks()
        self.roles_canvas.config(scrollregion=self.roles_canvas.bbox("all"))
    
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
        for widget in self.user_container.winfo_children():
            widget.destroy()

        users = self.controller.get_all_users()

        for user in users:
            self.add_user_row(user)
    
    def add_user_row(self, user):
        row = ctk.CTkFrame(self.user_container, fg_color="#1e293b")
        row.pack(fill="x", pady=5, padx=5)
        
        ctk.CTkLabel(
            row,
            text=user.id,
            text_color="white",
            width=50,
            anchor="w"
        ).pack(side="left", padx=10)

        label_username = ctk.CTkLabel(
            row,
            text=user.username,
            text_color="white",
            width=150,
            anchor="w"
        )
        label_username.pack(side="left", padx=10)
        label_username.bind("<Button-1>", lambda event, u=user: self.on_label_click(u))
        label_username.configure(cursor="hand2")

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

    def save_roles(self):
        if self.selected_user_id is None and self.roles:
            messagebox.showinfo("Atenção", "Selecione um perfil para salvar permissões.")
            return

        role = next((r for r in self.roles if r.id == self.selected_user_id), None)
        if not role:
            messagebox.showinfo("Atenção", "Perfil não encontrado.")
            return

        role_ids = [role_id for role_id, var in self.roles_vars.items() if var.get()]
        self.controller.set_roles_for_user(role.id, role_ids)
        messagebox.showinfo("Sucesso", f"Permissões salvas para {role.name}.")
        # 🔥 limpa depois de salvar
        self.clear_roles_selection()
        self.selected_user_id = None

    def get_roles_by_role(self, role_id):
        return self.service.get_roles_by_role(role_id)

    def on_label_click(self, user):
        self.selected_user_id = user.id
        self.load_roles_for_user(user.id)

        # resetar cores
        for widget in self.user_container.winfo_children():
            widget.configure(fg_color="#1e293b")

        # destacar selecionado
        for widget in self.user_container.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkLabel) and child.cget("text") == user.name:
                    widget.configure(fg_color="#334155")

    def load_roles_for_user(self, user_id):
        # limpa tudo primeiro
        self.clear_roles_selection()

        role_roles = self.controller.get_roles_by_user(user_id)

        # supondo que venha lista de objetos com .id
        for role in role_roles:
            if role.id in self.roles_vars:
                self.roles_vars[role.id].set(True)

    def clear_roles_selection(self):
        for var in self.roles_vars.values():
            var.set(False)

