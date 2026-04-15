from services.auth_service import AuthService
from services.cliente_robo_mysql_service import ClienteRoboMysqlService
from services.roles_service import RoleService
from services.user_service import UserService
from core.state import AppState

class Container:
    def __init__(self):
        self.state = AppState()
        self.auth_service = AuthService()
        self.user_service = UserService()
        self.role_service = RoleService()
        self.dashboard_service = ClienteRoboMysqlService()