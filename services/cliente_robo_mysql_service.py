from database.repositories.cliente_robo_mysql_repository import ClienteRoboMysqlRepository


class ClienteRoboMysqlService:
    def __init__(self):
        self.repo = ClienteRoboMysqlRepository()

    def carrega_robos_ativos(self, callback):
        return self.repo.carrega_robos_ativos(callback)