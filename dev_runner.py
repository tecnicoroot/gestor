"""
DEV RUNNER - AUTO RELOAD PARA DESENVOLVIMENTO

Este script monitora alterações nos arquivos do projeto e reinicia automaticamente
a aplicação (main.py).

Ideal para desenvolvimento com interfaces gráficas como CustomTkinter.

Requisitos:
    pip install watchdog
"""

import subprocess   # Para iniciar/parar o processo da aplicação
import sys          # Para pegar o interpretador Python atual
import time         # Para controle de tempo (debounce)
import os           # Para manipulação de caminhos
import signal       # Para lidar com encerramento correto do processo

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DevRunner(FileSystemEventHandler):
    """
    Classe responsável por:
    - Monitorar alterações nos arquivos
    - Reiniciar a aplicação automaticamente
    """

    def __init__(self):
        # Processo da aplicação (main.py)
        self.process = None

        # Controle de tempo para evitar múltiplos reloads seguidos
        self.last_run = 0

        # Inicia a aplicação pela primeira vez
        self.start_process()

    def start_process(self):
        """
        Inicia ou reinicia o processo da aplicação.
        """

        # Se já existe um processo rodando, encerra ele
        if self.process:
            print("🛑 Finalizando processo anterior...")
            self.process.terminate()   # encerra de forma segura
            self.process.wait()        # aguarda finalizar completamente

        print("🚀 Iniciando aplicação...")

        # Inicia o main.py usando o mesmo Python atual
        self.process = subprocess.Popen(
            [sys.executable, "main.py"]
        )

    def should_reload(self, path):
        """
        Define se o arquivo modificado deve causar reload.

        Aqui filtramos:
        - Apenas arquivos .py
        - Ignoramos pastas desnecessárias (.env, cache, etc)
        """

        # Pastas ignoradas (melhora performance e evita loops)
        ignored_dirs = {
            ".env",
            "venv",
            "__pycache__",
            ".git",
            ".idea",
            ".vscode",
            "node_modules"
        }

        # Normaliza o caminho e separa em partes
        parts = set(os.path.normpath(path).split(os.sep))

        # Se qualquer pasta ignorada estiver no caminho → ignora
        if parts & ignored_dirs:
            return False

        # Só reage a arquivos Python
        return path.endswith(".py")

    def on_modified(self, event):
        """
        Evento chamado quando um arquivo é modificado.
        """

        # Ignora diretórios (queremos só arquivos)
        if event.is_directory:
            return

        # Verifica se deve recarregar
        if not self.should_reload(event.src_path):
            return

        # Controle de debounce (evita múltiplos reloads rápidos)
        now = time.time()
        if now - self.last_run < 1:
            return

        self.last_run = now

        print(f"♻️ Alteração detectada: {event.src_path}")

        # Reinicia a aplicação
        self.start_process()


def main():
    """
    Função principal que inicia o monitoramento.
    """

    print(f"""
==============================
🔥 DEV RUNNER ATIVO
📂 Diretório: {os.getcwd()}
==============================
    """)

    # Cria o observer (monitor de arquivos)
    observer = Observer()

    # Instancia nosso handler
    handler = DevRunner()

    # Define que queremos monitorar a pasta atual (recursivo)
    observer.schedule(handler, path=".", recursive=True)

    # Inicia o monitoramento
    observer.start()

    print("👀 Monitorando alterações... (CTRL+C para sair)\n")

    try:
        # Loop infinito enquanto o programa roda
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        # Quando o usuário pressiona CTRL+C
        print("\n🛑 Encerrando DEV RUNNER...")

        observer.stop()

        # Encerra a aplicação também
        if handler.process:
            handler.process.terminate()

    # Aguarda o observer finalizar corretamente
    observer.join()


# Ponto de entrada do script
if __name__ == "__main__":
    main()