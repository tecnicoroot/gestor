import pandas as pd
import pymysql
from sshtunnel import SSHTunnelForwarder
from utils.decript import Decript
import re


class BancoDadosMysql:
    def __init__(self):
        self.dc = Decript()

    def _connect(self):
        pwd = self.dc.dm()
        ssh_host = 'dbmysqlnx'
        ssh_port = 22
        ssh_user = 'root'
        ssh_passwd = pwd.split(';')[16]

        sql_username = 'rpaujf'
        sql_password = pwd.split(';')[17]
        sql_database = 'bdrpajf'
        sql_hostname = '127.0.0.1'
        sql_port = 3306

        tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_user,
            ssh_password=ssh_passwd,
            remote_bind_address=(sql_hostname, sql_port)
        )
        tunnel.start()

        connection = pymysql.connect(
            host='127.0.0.1',
            user=sql_username,
            password=sql_password,
            db=sql_database,
            port=tunnel.local_bind_port,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

        return connection, tunnel

    def select(self, sql, params=None):
        """
        Executa um SELECT seguro no banco de dados.
        Aceita apenas comandos que comecem com SELECT.
        """
        try:
            if not re.match(r'^\s*SELECT\s', sql, re.IGNORECASE):
                raise ValueError("Apenas comandos SELECT são permitidos.")

            conn, tunnel = self._connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params if params else ())
                    rows = cursor.fetchall()
                    return rows
            finally:
                conn.close()
                tunnel.stop()
        except Exception as e:
            return f'Erro ao executar SELECT: {e}'

    def changedata(self, sql, tabela=None, params=None):
        """
        Executa comandos INSERT, UPDATE ou DELETE com parâmetros.
        Retorna o último ID inserido, se aplicável.
        """
        try:
            if not re.match(r'^\s*(INSERT|UPDATE|DELETE)\s', sql, re.IGNORECASE):
                raise ValueError("Apenas comandos INSERT, UPDATE ou DELETE são permitidos.")

            if tabela and not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', tabela):
                raise ValueError(f"Nome de tabela inválido: {tabela}")

            conn, tunnel = self._connect()
            try:
                with conn.cursor() as cursor:
                    cursor.execute(sql, params if params else ())
                    conn.commit()

                    if sql.strip().lower().startswith('insert') and tabela:
                        cursor.execute(f"SELECT MAX(id) as ultimo FROM {tabela}")
                        result = cursor.fetchone()
                        return result['ultimo']
                    return None
            finally:
                conn.close()
                tunnel.stop()
        except Exception as e:
            return f'Erro ao executar alteração no banco: {e}'


if __name__ == '__main__':
   pass
