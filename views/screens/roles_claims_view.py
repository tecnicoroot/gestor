import bcrypt
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from controllers.roles_controller import RolesController
from models.models import Role

class RolesClaimsView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container
        self.controller = RolesController(self, container)

        self.status_display_to_db = {
            "Ativo": "ACTIVE",
            "Inativo": "INACTIVE",
            "Suspenso": "SUSPENDED"
        }
        self.status_db_to_display = {v: k for k, v in self.status_display_to_db.items()}

        self.configure(fg_color="#0f172a")

        # FRAME DE DUAS COLUNAS
        self.columns_frame = ctk.CTkFrame(self, fg_color="#0f172a")
        self.columns_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # =========================
        # 📦 COLUNA 1: CADASTRO E LISTA DE ROLES
        # =========================
        self.left_frame = ctk.CTkFrame(self.columns_frame, fg_color="#0f172a", corner_radius=15)
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=0)
        self.columns_frame.grid_columnconfigure(0, weight=1, minsize=420)
        self.columns_frame.grid_columnconfigure(1, weight=2)

        # ---- Cadastro
        ctk.CTkLabel(
            self.left_frame,
            text="Cadastro de Perfis",
            font=("Arial", 22, "bold"),
            text_color="white"
        ).pack(pady=20)

        entries_frame = ctk.CTkFrame(self.left_frame, fg_color="transparent")
        entries_frame.pack(pady=10)

        self.name = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Nome",
            width=300,
            height=40,
            corner_radius=10
        )
        self.name.pack(pady=10)

        self.descricao = ctk.CTkEntry(
            entries_frame,
            placeholder_text="Descrição",
            width=300,
            height=40,
            corner_radius=10
        )
        self.descricao.pack(pady=10)

        # Campo de status
        #self.add_status_entry = ctk.CTkComboBox(
        #    entries_frame,
        #    values=list(self.status_display_to_db.keys()),
        #    width=300,
        #    corner_radius=10
        #)
        #self.add_status_entry.set("Ativo")
        #self.add_status_entry.pack(pady=10)

        ctk.CTkButton(
            self.left_frame,
            text="Salvar Perfil",
            width=150,
            height=40,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=self.save_role
        ).pack(pady=15)

        ctk.CTkButton(
            self.left_frame,
            text="Voltar",
            width=150,
            height=35,
            fg_color="#334155",
            hover_color="#475569",
            command=lambda: self.router.navigate("dashboard")
        ).pack(pady=5)

        self.message_label = ctk.CTkLabel(
            self.left_frame,
            text="",
            text_color="#94a3b8"
        )
        self.message_label.pack(pady=10)

        # ---- Lista de Roles
        
        self.roles_container = ctk.CTkScrollableFrame(self.left_frame, fg_color="#1e293b", width=450, height=353)
        self.roles_container.pack(fill="x", expand=False, padx=5, pady=5)

        # =========================
        # 📦 COLUNA 2: CLAIMS
        # =========================
        self.right_frame = ctk.CTkFrame(self.columns_frame, fg_color="#fff9c4")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 0), pady=0)

        ctk.CTkLabel(self.right_frame, text="Acessos Disponíveis",
                     font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(12, 4), anchor="center")

        self.labels_frame = ctk.CTkFrame(self.right_frame, fg_color="#fff9c4")
        self.labels_frame.pack(pady=(0, 8), anchor="w")
        ctk.CTkFrame(self.right_frame, height=2, fg_color="#aee1ab").pack(fill="x", padx=5, pady=(0, 10))
        label_width = 120
        for label_text in ["Cadastrar", "Visualizar", "Atualizar", "Apagar"]:
            ctk.CTkLabel(self.labels_frame, text=label_text, font=ctk.CTkFont(size=14, weight="bold"),
                         width=label_width, anchor="center").pack(side="left", padx=0)

        self.claims_outer_frame = ctk.CTkFrame(self.right_frame, fg_color="#fff9c4")
        self.claims_outer_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.claims_canvas = tk.Canvas(self.claims_outer_frame, bg="#fff9c4", highlightthickness=0)
        self.claims_canvas.pack(side="left", fill="both", expand=True)
        self.claims_scrollbar = tk.Scrollbar(self.claims_outer_frame, orient="vertical",
                                             command=self.claims_canvas.yview)
        self.claims_scrollbar.pack(side="right", fill="y")
        self.claims_canvas.configure(yscrollcommand=self.claims_scrollbar.set)
        self.claims_grid = ctk.CTkFrame(self.claims_canvas, fg_color="#fff9c4")
        self.claims_canvas.create_window((0, 0), window=self.claims_grid, anchor="nw")

        ctk.CTkButton(self.right_frame, text="Salvar Permissões", command=self.save_claims).pack(pady=12)

        # --- DADOS INTERNOS ---
        self.roles = []
        self.claims = []
        self.claims_vars = {}
        self.claims_widgets = {}
        self.selected_role_id = None

        self.load_roles()
        self.load_claims()

    def load_claims(self):
        # Limpa checkboxes antigos
        for widget in self.claims_grid.winfo_children():
            widget.destroy()
        self.claims = self.controller.get_all_claims()
        self.claims_vars.clear()
        self.claims_widgets.clear()
        columns = 4
        checkboxes_per_group = 4

        columns_claims = [[] for _ in range(columns)]
        for idx, claim in enumerate(self.claims):
            col = idx % columns
            columns_claims[col].append(claim)
        max_column_length = max(len(col_claims) for col_claims in columns_claims) if columns_claims else 0
        row_counter = 1

        for row in range(max_column_length):
            for col in range(columns):
                if row < len(columns_claims[col]):
                    claim = columns_claims[col][row]
                    var = ctk.BooleanVar()
                    cb = ctk.CTkCheckBox(self.claims_grid, text=f"{claim.value}", variable=var)
                    cb.grid(row=row_counter, column=col, sticky="w", padx=6, pady=2)
                    self.claims_vars[claim.id] = var
                    self.claims_widgets[claim.id] = cb
            row_counter += 1
            if (row + 1) % checkboxes_per_group == 0 and (row + 1) < max_column_length:
                sep = ctk.CTkFrame(self.claims_grid, height=2, fg_color="#000000")
                sep.grid(row=row_counter, column=0, columnspan=columns, sticky="we", pady=4)
                row_counter += 1

        self.claims_grid.update_idletasks()
        self.claims_canvas.config(scrollregion=self.claims_canvas.bbox("all"))

    def save_role(self):
        role = self.get_role_from_inputs()
        if hasattr(self, "editing_role_id"):
            role.id = self.editing_role_id
            self.controller.update_role(role)
            del self.editing_role_id
        else:
            self.controller.create_role(role)

        self.limpa_inputs()
        self.load_roles()

    def show_success(self, msg):
        self.message_label.configure(text=msg, text_color="#22c55e")

    def show_error(self, msg):
        self.message_label.configure(text=msg, text_color="#ef4444")

    def destroy(self):
        try:
            self.name.unbind("<Return>")
            self.descricao.unbind("<Return>")
        except:
            pass
        super().destroy()

    def load_roles(self):
        for widget in self.roles_container.winfo_children():
            widget.destroy()

        self.roles = self.controller.get_all_roles()
        for role in self.roles:
            self.add_role_row(role)

    def add_role_row(self, role):
        row = ctk.CTkFrame(self.roles_container, fg_color="#1e293b")
        row.pack(fill="x", pady=5, padx=5)

        ctk.CTkLabel(
            row,
            text=role.id,
            text_color="white",
            
            anchor="w"
        ).pack(side="left", padx=10)

        label_name = ctk.CTkLabel(
            row,
            text=role.name,
            text_color="white",
            width=100,
            anchor="w"
        )
        label_name.pack(side="left", padx=10)
        label_name.bind("<Button-1>", lambda event, r=role: self.on_label_click(r))
        label_name.configure(cursor="hand2")


        #ctk.CTkLabel(
        #    row,
        #    text=role.description,
        #    text_color="#94a3b8",
        #    width=100
        #).pack(side="left")

        ctk.CTkButton(
            row,
            text="Editar",
            width=70,
            fg_color="#eab308",
            hover_color="#ca8a04",
            command=lambda u=role: self.edit_role(u)
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            row,
            text="Excluir",
            width=70,
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=lambda u=role.id: self.delete_role(u)
        ).pack(side="right", padx=5)

    def get_role_from_inputs(self):
        status_display = self.add_status_entry.get()
        status_db = self.status_display_to_db.get(status_display, "ACTIVE")
        return Role(
            name=self.name.get(),
            description=self.descricao.get(),
            #status=status_db
        )

    def limpa_inputs(self):
        self.name.delete(0, "end")
        self.descricao.delete(0, "end")
        self.add_status_entry.set("Ativo")

    def delete_role(self, role_id):
        
        self.controller.delete_role(role_id)
        self.load_roles()

    def edit_role(self, role):
        self.limpa_inputs()
        self.name.insert(0, role.name)
        self.descricao.insert(0, role.description)
        self.add_status_entry.set(self.status_db_to_display.get(role.status, "Ativo"))
        self.editing_role_id = role.id

    def save_claims(self):
        if self.selected_role_id is None and self.roles:
            messagebox.showinfo("Atenção", "Selecione um perfil para salvar permissões.")
            return

        role = next((r for r in self.roles if r.id == self.selected_role_id), None)
        if not role:
            messagebox.showinfo("Atenção", "Perfil não encontrado.")
            return

        claim_ids = [claim_id for claim_id, var in self.claims_vars.items() if var.get()]
        self.controller.set_claims_for_role(role.id, claim_ids)
        messagebox.showinfo("Sucesso", f"Permissões salvas para {role.name}.")
        # 🔥 limpa depois de salvar
        self.clear_claims_selection()
        self.selected_role_id = None

    def get_claims_by_role(self, role_id):
        return self.service.get_claims_by_role(role_id)
    
    def on_label_click(self, role):
        self.selected_role_id = role.id
        self.load_claims_for_role(role.id)

        # resetar cores
        for widget in self.roles_container.winfo_children():
            widget.configure(fg_color="#1e293b")

        # destacar selecionado
        for widget in self.roles_container.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, ctk.CTkLabel) and child.cget("text") == role.name:
                    widget.configure(fg_color="#334155")
    
    def load_claims_for_role(self, role_id):
        # limpa tudo primeiro
        self.clear_claims_selection()

        role_claims = self.controller.get_claims_by_role(role_id)

        # supondo que venha lista de objetos com .id
        for claim in role_claims:
            if claim.id in self.claims_vars:
                self.claims_vars[claim.id].set(True)

    def clear_claims_selection(self):
        for var in self.claims_vars.values():
            var.set(False)