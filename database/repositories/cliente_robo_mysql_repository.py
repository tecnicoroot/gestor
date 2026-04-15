import threading

from database.bancodadosmysql import BancoDadosMysql

class ClienteRoboMysqlRepository:
    def __init__(self):
        self.bd = BancoDadosMysql()

    def _handle_result(self, resultado):
        if isinstance(resultado, str):
            print("ERRO:", resultado)
            return []
        return resultado

    def contar_robos(self):
        resultado = self.bd.select("SELECT COUNT(*) AS total FROM robos")
        if isinstance(resultado, str):
            print("Erro ao contar:", resultado)
            return 0
        return resultado[0]["total"]

    def carregar_robos_pagina(self, pagina=1, por_pagina=20):
        offset = (pagina - 1) * por_pagina
        sql = f"SELECT * FROM robos LIMIT {por_pagina} OFFSET {offset}"
        robos = self._handle_result(self.bd.select(sql))
        total = self.contar_robos()
        return robos, pagina, total, por_pagina

    def carregar_robos(self, callback, sql):
        threading.Thread(target=self._carregar_robos_thread, args=(callback,sql), daemon=True).start()

    def _carregar_robos_thread(self, callback, sql):
        robos = self._handle_result(self.bd.select(sql))
        callback(robos)
        # Aqui deveria chamar um callback ou enviar para uma fila

    def adicionar_robo(self, dados):
        campos = ", ".join([k for k in dados if k != "id"])
        valores = ", ".join(["%s"] * (len(dados) - 1))
        params = tuple([dados[k] for k in dados if k != "id"])
        sql = f"INSERT INTO robos ({campos}) VALUES ({valores})"
        resultado = self.bd.changedata(sql, "robos", params)
        if isinstance(resultado, str):
            print("ERRO AO INSERIR:", resultado)
        return resultado

    def editar_robo(self, id_robo, novos_dados):
        set_str = ", ".join([f"{k}=%s" for k in novos_dados if k != "id"])
        params = tuple([novos_dados[k] for k in novos_dados if k != "id"] + [id_robo])
        sql = f"UPDATE robos SET {set_str} WHERE id=%s"
        resultado = self.bd.changedata(sql, "robos", params)
        if isinstance(resultado, str):
            print("ERRO AO ATUALIZAR:", resultado)
        return resultado

    def excluir_robo(self, id_robo):
        sql = "DELETE FROM robos WHERE id=%s"
        resultado = self.bd.changedata(sql, "robos", (id_robo,))
        if isinstance(resultado, str):
            print("ERRO AO EXCLUIR:", resultado)
        return resultado

    def buscar_robo(self, id_robo):
        sql = "SELECT * FROM robos WHERE id=%s"
        robos = self._handle_result(self.bd.select(sql, (id_robo,)))
        return robos[0] if robos else None

    def carrega_robos_ativos(self, callback):

        base_query = (
            '''select a.nome, 
                a.id, a.descricao, a.ativo, b.start, 
                b.finished, b.ativa, b.server
                FROM bdrpajf.robos a 
                INNER JOIN  (
                                SELECT
                                    idrobo,
                                    MAX(ID) AS max_id
                                FROM
                                    bdrpajf.fila
                                GROUP BY
                                    idrobo
                            ) ult_fila ON ult_fila.idrobo = a.id
                INNER JOIN bdrpajf.fila b ON b.idrobo = a.ID AND b.id = ult_fila.max_id where b.ativa = 's' '''

        )
        return self.carregar_robos(callback, base_query)

if __name__ == "__main__":
    repo = ClienteRoboMysqlRepository()
    robo = repo.buscar_robo(1)
    import pprint
    pprint.pprint(robo)