class AppState:
    def __init__(self):
        self.user = None          # Pode ser um objeto User ou apenas um dict/string
        self.roles = []         # Lista de roles
        self.claims = {}        # Dicionário de claims
        self.preferences = {}   # Outras preferências do usuário (opcional)

    def is_in_role(self, role):
        return role in self.roles

    def has_claim(self, claim):
        return self.claims.get(claim, False)

    def clear(self):
        """Reseta o estado, útil para logout"""
        self.user = None
        self.roles = []
        self.claims = {}
        self.preferences = {}