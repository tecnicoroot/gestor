import customtkinter as ctk
import socket
import threading
import datetime
import os

try:
    import winsound
    beep = lambda: winsound.MessageBeep()
except ImportError:
    beep = lambda: None

HISTORICO_PATH = "chat_historico.txt"

class P2PChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat P2P Aprimorado")
        self.geometry("600x500")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Nome do usuário
        ctk.CTkLabel(self, text="Seu nome:").pack()
        self.nome_entry = ctk.CTkEntry(self, width=160)
        self.nome_entry.pack()
        self.nome_entry.insert(0, os.getlogin())

        # Porta local
        ctk.CTkLabel(self, text="Sua porta local:").pack()
        self.local_port_entry = ctk.CTkEntry(self, width=80)
        self.local_port_entry.pack()
        self.local_port_entry.insert(0, "54321")

        # IP/porta do destino
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5)
        ctk.CTkLabel(frame, text="IP Destino:").pack(side="left")
        self.ip_entry = ctk.CTkEntry(frame, width=120)
        self.ip_entry.pack(side="left", padx=3)
        self.ip_entry.insert(0, "127.0.0.1")
        ctk.CTkLabel(frame, text="Porta:").pack(side="left")
        self.port_entry = ctk.CTkEntry(frame, width=80)
        self.port_entry.pack(side="left", padx=3)
        self.port_entry.insert(0, "54321")

        # Mensagens
        self.textbox = ctk.CTkTextbox(self, height=250, width=500)
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)
        self.carregar_historico()

        # Campo mensagem
        self.msg_entry = ctk.CTkEntry(self, width=350)
        self.msg_entry.pack(padx=10, pady=5, fill="x")
        self.msg_entry.bind("<Return>", self.enviar_mensagem)

        # Botão enviar
        self.button = ctk.CTkButton(self, text="Enviar", command=self.enviar_mensagem)
        self.button.pack(pady=3)

        # Servidor socket
        self.servidor_socket = None
        self.servidor_thread = None
        self.iniciar_servidor()

    def carregar_historico(self):
        if os.path.exists(HISTORICO_PATH):
            with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
                for linha in f:
                    self.textbox.insert("end", linha)
            self.textbox.see("end")

    def salvar_historico(self, linha):
        with open(HISTORICO_PATH, "a", encoding="utf-8") as f:
            f.write(linha)

    def iniciar_servidor(self):
        try:
            porta = int(self.local_port_entry.get())
        except ValueError:
            self.textbox.insert("end", "Porta inválida para servidor!\n")
            return
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.servidor_socket.bind(('', porta))
            self.servidor_socket.listen(5)
            self.textbox.insert("end", f"[{self.hora()}] Servidor escutando na porta {porta}\n")
            self.servidor_thread = threading.Thread(target=self.escutar_mensagens, daemon=True)
            self.servidor_thread.start()
        except Exception as e:
            self.textbox.insert("end", f"Erro ao iniciar servidor: {e}\n")

    def escutar_mensagens(self):
        while True:
            try:
                conn, addr = self.servidor_socket.accept()
                threading.Thread(target=self.ler_cliente, args=(conn, addr), daemon=True).start()
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Erro no servidor: {e}\n"))
                break

    def ler_cliente(self, conn, addr):
        try:
            data = conn.recv(4096)
            if data:
                msg = data.decode()
                # Mensagem esperada: nome:mensagem
                if ':' in msg:
                    nome, texto = msg.split(':', 1)
                else:
                    nome, texto = 'Remoto', msg
                linha = f"[{self.hora()}] {nome.strip()}: {texto.strip()}\n"
                self.after(0, lambda: self.exibir_mensagem(linha, recebido=True))
                self.salvar_historico(linha)
                beep()
        except Exception as e:
            self.after(0, lambda: self.textbox.insert("end", f"Erro na leitura: {e}\n"))
        finally:
            conn.close()

    def enviar_mensagem(self, event=None):
        ip = self.ip_entry.get()
        try:
            porta = int(self.port_entry.get())
        except ValueError:
            self.textbox.insert("end", "Porta de destino inválida!\n")
            return
        msg = self.msg_entry.get().strip()
        if not msg:
            return
        nome_usuario = self.nome_entry.get().strip() or "Você"
        texto_envio = f"{nome_usuario}:{msg}"
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, porta))
            s.sendall(texto_envio.encode())
            s.close()
            linha = f"[{self.hora()}] {nome_usuario} (você): {msg}\n"
            self.exibir_mensagem(linha, recebido=False)
            self.salvar_historico(linha)
            self.msg_entry.delete(0, "end")
        except Exception as e:
            self.textbox.insert("end", f"Falha ao enviar: {e}\n")
            self.textbox.see("end")

    def exibir_mensagem(self, linha, recebido=False):
        # Você pode customizar colorindo texto com emojis, prefixos, etc.
        self.textbox.insert("end", linha)
        self.textbox.see("end")

    def hora(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def on_close(self):
        try:
            if self.servidor_socket:
                self.servidor_socket.close()
        except:
            pass
        self.destroy()

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = P2PChatApp()
    app.mainloop()