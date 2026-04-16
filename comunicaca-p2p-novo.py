import customtkinter as ctk
from tkinter import filedialog
from plyer import notification
import socket
import threading
import os
import datetime

PORTA_PADRAO = 54321

class P2PChatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chat P2P - Arquivos & Notificação")
        self.geometry("620x500")
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

        # Servidor socket
        self.servidor_socket = None
        self.servidor_thread = None
        self.iniciar_servidor()

        # Pasta para arquivos recebidos
        self.recebidos_dir = "arquivos_recebidos"
        os.makedirs(self.recebidos_dir, exist_ok=True)

    def hora(self):
        return datetime.datetime.now().strftime("%H:%M:%S")

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
            # Primeiro, lê o cabeçalho, até encontrar \n
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
                # Cabeçalho: FILE:<nome>:<tamanho>
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
                # Mensagem normal: <nome>:<mensagem>
                data = b""
                while True:
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                msg = data.decode()
                if ':' in header_str:
                    nome, texto = header_str.split(':', 1)
                    texto = texto + msg  # Se mensagem era longa, vem parte no data
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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((ip, porta))
            s.sendall(texto_envio.encode())
            s.close()
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
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(8)
            s.connect((ip, port))
            header = f"FILE:{nome_arquivo}:{len(dados)}\n".encode()
            s.sendall(header + dados)
            s.close()
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
            # Pode falhar em ambientes sem suporte (ex: WSL)
            pass

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