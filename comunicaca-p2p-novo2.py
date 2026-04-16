import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from plyer import notification
import socket
import ssl
import threading
import os
import datetime
import json

PORTA_PADRAO = 54321
CERT_FILE = "cert.pem"
KEY_FILE = "key.pem"
CONTATOS_FILE = "contatos.json"

class P2PChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat P2P - SSL & Contatos")
        self.geometry("670x520")
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
        self.local_port_entry.insert(0, str(PORTA_PADRAO))

        # Lista de contatos
        self.contatos = self.carregar_contatos()
        contatos_nomes = [c['nome'] for c in self.contatos] if self.contatos else []
        ctk.CTkLabel(self, text="Contatos:").pack()
        self.contato_combo = ctk.CTkComboBox(self, values=contatos_nomes, width=220)
        self.contato_combo.pack()
        self.contato_combo.bind("<<ComboboxSelected>>", self.preencher_destino_contato)

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
        self.port_entry.insert(0, str(PORTA_PADRAO))

        # Mensagens
        self.textbox = ctk.CTkTextbox(self, height=250, width=500)
        self.textbox.pack(padx=10, pady=10, fill="both", expand=True)

        # Campo mensagem
        self.msg_entry = ctk.CTkEntry(self, width=350)
        self.msg_entry.pack(padx=10, pady=5, fill="x")
        self.msg_entry.bind("<Return>", self.enviar_mensagem)

        # Botões
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=3)
        self.button = ctk.CTkButton(btn_frame, text="Enviar Mensagem", command=self.enviar_mensagem)
        self.button.pack(side="left", padx=5)
        self.btn_arquivo = ctk.CTkButton(btn_frame, text="Enviar Arquivo", command=self.enviar_arquivo)
        self.btn_arquivo.pack(side="left", padx=5)
        self.btn_add_contato = ctk.CTkButton(btn_frame, text="Adicionar Contato", command=self.adicionar_contato)
        self.btn_add_contato.pack(side="left", padx=5)

        # Servidor socket (SSL)
        self.servidor_socket = None
        self.servidor_thread = None
        self.ssl_context = None
        self.iniciar_servidor_ssl()

        # Pasta para arquivos recebidos
        self.recebidos_dir = "arquivos_recebidos"
        os.makedirs(self.recebidos_dir, exist_ok=True)

    def hora(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

    def iniciar_servidor_ssl(self):
        try:
            porta = int(self.local_port_entry.get())
        except ValueError:
            self.textbox.insert("end", "Porta inválida para servidor!\n")
            return
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
#        self.ssl_context.load_cert_chain(certfile=CERT_FILE, keyfile=KEY_FILE)
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.servidor_socket.bind(('', porta))
            self.servidor_socket.listen(5)
            self.textbox.insert("end", f"[{self.hora()}] Servidor SSL escutando na porta {porta}\n")
            self.servidor_thread = threading.Thread(target=self.escutar_mensagens_ssl, daemon=True)
            self.servidor_thread.start()
        except Exception as e:
            self.textbox.insert("end", f"Erro ao iniciar servidor: {e}\n")

    def escutar_mensagens_ssl(self):
        while True:
            try:
                newsocket, addr = self.servidor_socket.accept()
                conn = self.ssl_context.wrap_socket(newsocket, server_side=True)
                threading.Thread(target=self.ler_cliente, args=(conn, addr), daemon=True).start()
            except Exception as e:
                self.after(0, lambda: self.textbox.insert("end", f"Erro no servidor: {e}\n"))
                break

    def ler_cliente(self, conn, addr):
        try:
            header = b""
            while not header.endswith(b"\n"):
                chunk = conn.recv(1)
                if not chunk:
                    break
                header += chunk
            if not header:
                return
            header_str = header.decode().strip()
            if header_str.startswith("FILE:"):
                _, nome, tamanho = header_str.split(":")
                tamanho = int(tamanho)
                filedata = b""
                while len(filedata) < tamanho:
                    parte = conn.recv(min(4096, tamanho - len(filedata)))
                    if not parte:
                        break
                    filedata += parte
                filepath = os.path.join(self.recebidos_dir, f"{self.hora().replace(':','-')}_{nome}")
                with open(filepath, "wb") as f:
                    f.write(filedata)
                msg = f"[{self.hora()}] Arquivo '{nome}' recebido de {addr[0]} salvo como '{filepath}'\n"
                self.after(0, lambda: self.textbox.insert("end", msg))
                self.after(0, lambda: self.textbox.see("end"))
                self.notificar_bandeja("Arquivo recebido", f"Arquivo '{nome}' de {addr[0]}")
            else:
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                msg = data.decode()
                if ':' in header_str:
                    nome, texto = header_str.split(':', 1)
                    texto = texto + msg
                else:
                    nome, texto = "Remoto", header_str + msg
                linha = f"[{self.hora()}] {nome.strip()}: {texto.strip()}\n"
                self.after(0, lambda: self.exibir_mensagem(linha, recebido=True))
                self.notificar_bandeja("Nova mensagem", f"De {nome.strip()}")
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
        texto_envio = f"{nome_usuario}:{msg}\n"
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            ssl_sock = context.wrap_socket(s)
            ssl_sock.connect((ip, porta))
            ssl_sock.sendall(texto_envio.encode())
            ssl_sock.close()
            linha = f"[{self.hora()}] {nome_usuario} (você): {msg}\n"
            self.exibir_mensagem(linha, recebido=False)
            self.msg_entry.delete(0, "end")
        except Exception as e:
            self.textbox.insert("end", f"Falha ao enviar: {e}\n")
            self.textbox.see("end")

    def enviar_arquivo(self):
        file_path = filedialog.askopenfilename()
        if not file_path:
            return
        ip = self.ip_entry.get()
        try:
            port = int(self.port_entry.get())
        except ValueError:
            self.textbox.insert("end", "Porta de destino inválida!\n")
            return
        nome_arquivo = os.path.basename(file_path)
        try:
            with open(file_path, "rb") as f:
                dados = f.read()
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(8)
            ssl_sock = context.wrap_socket(s)
            ssl_sock.connect((ip, port))
            header = f"FILE:{nome_arquivo}:{len(dados)}\n".encode()
            ssl_sock.sendall(header + dados)
            ssl_sock.close()
            self.textbox.insert("end", f"[{self.hora()}] Arquivo '{nome_arquivo}' enviado!\n")
            self.textbox.see("end")
        except Exception as e:
            self.textbox.insert("end", f"Erro ao enviar arquivo: {e}\n")

    def exibir_mensagem(self, linha, recebido=False):
        self.textbox.insert("end", linha)
        self.textbox.see("end")

    def notificar_bandeja(self, titulo, msg):
        try:
            notification.notify(
                title=titulo,
                message=msg,
                timeout=5
            )
        except Exception as e:
            pass

    def on_close(self):
        try:
            if self.servidor_socket:
                self.servidor_socket.close()
        except:
            pass
        self.destroy()

    def carregar_contatos(self):
        if os.path.isfile(CONTATOS_FILE):
            with open(CONTATOS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def salvar_contatos(self):
        with open(CONTATOS_FILE, "w", encoding="utf-8") as f:
            json.dump(self.contatos, f, ensure_ascii=False, indent=2)

    def adicionar_contato(self):
        nome = self.nome_entry.get().strip()
        ip = self.ip_entry.get().strip()
        porta = self.port_entry.get().strip()
        if not nome or not ip or not porta:
            messagebox.showerror("Erro", "Preencha nome, IP e porta para adicionar contato.")
            return
        if any(c["nome"] == nome for c in self.contatos):
            messagebox.showwarning("Atenção", "Contato já existe com esse nome.")
            return
        novo = {"nome": nome, "ip": ip, "porta": int(porta)}
        self.contatos.append(novo)
        self.salvar_contatos()
        self.contato_combo.configure(values=[c['nome'] for c in self.contatos])
        messagebox.showinfo("Contato", f"Contato '{nome}' adicionado!")

    def preencher_destino_contato(self, event=None):
        nome = self.contato_combo.get()
        c = next((x for x in self.contatos if x["nome"] == nome), None)
        if c:
            self.ip_entry.delete(0, "end")
            self.ip_entry.insert(0, c["ip"])
            self.port_entry.delete(0, "end")
            self.port_entry.insert(0, str(c["porta"]))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = P2PChatApp()
    app.mainloop()

# openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem

#1. Instale o OpenSSL no Windows
#Acesse:
#https://slproweb.com/products/Win32OpenSSL.html

#Baixe e instale a versão adequada do Win64 OpenSSL (geralmente a “Light” já serve).
# openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem