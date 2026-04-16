import customtkinter as ctk
import datetime
from controllers.dashboard_controller import DashboardController


class DashboardView(ctk.CTkFrame):
    def __init__(self, app, router, container):
        super().__init__(app)

        self.app = app
        self.router = router
        self.container = container
        self.controller = DashboardController(self, container)
        # 🌑 fundo geral (mesmo do login)
        self.configure(fg_color="#0f172a")

        self.cards = []
        self.cards_ativos = []

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




        ctk.CTkLabel(
            self.sidebar,
            text="ERP SYSTEM",
            font=("Arial", 18, "bold"),
            text_color="white"
        ).pack(pady=20)

        # =========================
        # 📦 CONTEÚDO PRINCIPAL
        # =========================
        self.content = ctk.CTkFrame(
            self,
            fg_color="#0f172a"
        )
        self.content.pack(side="left", fill="both", expand=True)

        self.show_home()
        print(self.container.state.user.name)
        print(self.container.state.roles)
        print(self.container.state.claims)
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
        self.card_frame = ctk.CTkFrame(self.content, fg_color="transparent")
        self.card_frame.pack(pady=20)

        self.controller.service.carrega_robos_ativos(self.lista_robos_ativos)
    # =========================
    # CARD COMPONENT
    # =========================
    def create_card(self, parent, id, nome, inicio, fim, servidor, row, column):

        card = ctk.CTkFrame(parent, width=300, height=200, fg_color="#1e293b", corner_radius=15)
        card.grid(row=row, column=column, padx=10, pady=10)
        card.pack_propagate(False)  # Garante tamanho fixo
        ctk.CTkLabel(
            card,
            text=id,
            text_color="#94a3b8",
            font=("Arial", 20)
        ).pack(pady=10)

        ctk.CTkLabel(
            card,
            text=nome,
            text_color="white",
            font=("Arial", 15, "bold")
        ).pack()

        ctk.CTkLabel(
            card,
            text=inicio,
            text_color="white",
            font=("Arial", 15, "bold")
        ).pack()

        ctk.CTkLabel(
            card,
            text= fim if fim not in [None, "None", ""] else "Em execução",
            text_color="white",
            font=("Arial", 15, "bold")
        ).pack()

        ctk.CTkLabel(
            card,
            text=servidor,
            text_color="white",
            font=("Arial", 15, "bold")
        ).pack()


        if inicio:
            tempo_exec = datetime.datetime.now() - inicio
            horas, resto = divmod(tempo_exec.seconds, 3600)
            minutos, segundos = divmod(resto, 60)
            texto_tempo = f"Tempo de execução: {horas:02d}:{minutos:02d}:{segundos:02d}"
        else:
            texto_tempo = "Tempo de execução: N/A"

        tempo_label = ctk.CTkLabel(
            card,
            text=texto_tempo,
            text_color="red",
            font=("Arial", 15, "bold")
        )
        tempo_label.pack()
        self.cards_ativos_labels.append({'label': tempo_label, 'start': inicio})
        self.update_tempo_execucao_ativos()


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
        self.container.state.clear()
        self.router.navigate("login")

    def carrega_robos_ativos(self):
        self.controller.service.carrega_robos_ativos(self.lista_robos_ativos)

    def lista_robos_ativos(self, robos):
        self.cards_ativos = []
        self.cards_ativos_labels = []

        def atualizar_gui():
            max_cards = 3
            for i, robo in enumerate(robos):
                row = i // max_cards
                col = i % max_cards
                self.create_card(
                    self.card_frame,
                    f"{robo['id']}", f"{robo['nome']}",
                    robo.get('start'), robo.get('finished'), robo.get('server'),
                    row, col
                )

        self.after(0, atualizar_gui)

        self.schedule_update_robos_ativos()

    def update_tempo_execucao_ativos(self):
        """Atualiza o tempo de execução dos robôs ativos em tempo real."""
        now = datetime.datetime.now()
        for item in getattr(self, 'cards_ativos_labels', []):
            label = item['label']
            start = item['start']
            if start:
                tempo_exec = now - start
                horas, resto = divmod(tempo_exec.seconds, 3600)
                minutos, segundos = divmod(resto, 60)
                texto_tempo = f"Tempo de execução: {horas:02d}:{minutos:02d}:{segundos:02d}"
            else:
                texto_tempo = "Tempo de execução: N/A"
            label.configure(text=texto_tempo)
        # Atualize a cada segundo
        self.after(1000, self.update_tempo_execucao_ativos)

    def schedule_update_robos_ativos(self):
        # Agenda a atualização dos cards ativos a cada 10 segundos (10000 ms)
        self.after(10000, self.carrega_robos_ativos)

    def on_show(self):
        self.refresh()

    def refresh(self):
        for widget in self.sidebar.pack_slaves():
            if isinstance(widget, ctk.CTkLabel) and widget.cget("text") != "ERP SYSTEM":
                widget.destroy()
        user = self.container.state.user
        user_obj = user

        ctk.CTkLabel(
            self.sidebar,
            text=f"{user_obj.username}",
            text_color="#94a3b8",
            font=("Arial", 12)
        ).pack(pady=5)

        for widget in self.sidebar.pack_slaves():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
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
            text="Sair",
            fg_color="#ef4444",
            hover_color="#b91c1c",
            command=self.logout
        ).pack(side="bottom", fill="x", padx=10, pady=20)