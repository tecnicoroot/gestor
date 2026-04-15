
class Robo:

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome):
        self._nome = nome

    @property
    def descricao(self):
        return self._descricao

    @descricao.setter
    def descricao(self, descricao):
        self._descricao = descricao

    @property
    def ativo(self):
        return self._ativo

    @ativo.setter
    def ativo(self, ativo):
        self._ativo = ativo

    @property
    def intervalo(self):
        return self._intervalo

    @intervalo.setter
    def intervalo(self, intervalo):
        self._intervalo = intervalo

    @property
    def acao(self):
        return self._acao

    @acao.setter
    def acao(self, acao):
        self._acao = acao

    @property
    def tela(self):
        return self._tela

    @tela.setter
    def tela(self, tela):
        self._tela = tela

    @property
    def path_executavel(self):
        return self._path_executavel

    @path_executavel.setter
    def path_executavel(self, path_executavel):
        self._path_executavel = path_executavel

    @property
    def limite_tempo(self):
        return self._limite_tempo

    @limite_tempo.setter
    def limite_tempo(self, limite_tempo):
        self._limite_tempo = limite_tempo

    @property
    def arquivo_ativacao(self):
        return self._arquivo_ativacao

    @arquivo_ativacao.setter
    def arquivo_ativacao(self, arquivo_ativacao):
        self._arquivo_ativacao = arquivo_ativacao

    @property
    def nome_executavel(self):
        return self._nome_executavel

    @nome_executavel.setter
    def nome_executavel(self, nome_executavel):
        self._nome_executavel = nome_executavel

    @property
    def pasta_trabalho(self):
        return self._pasta_trabalho

    @pasta_trabalho.setter
    def pasta_trabalho(self, pasta_trabalho):
        self._pasta_trabalho = pasta_trabalho

    @property
    def repositorio_planilhas(self):
        return self._repositorio_planilhas

    @repositorio_planilhas.setter
    def repositorio_planilhas(self, repositorio_planilhas):
        self._repositorio_planilhas = repositorio_planilhas

    @property
    def notificados(self):
        return self._notificados

    @notificados.setter
    def notificados(self, notificados):
        self._notificados = notificados

    @property
    def pgm_ativado1(self):
        return self._pgm_ativado1

    @pgm_ativado1.setter
    def pgm_ativado1(self, pgm_ativado1):
        self._pgm_ativado1 = pgm_ativado1

    @property
    def pgm_ativado2(self):
        return self._pgm_ativado2

    @pgm_ativado2.setter
    def pgm_ativado2(self, pgm_ativado2):
        self._pgm_ativado2 = pgm_ativado2

    @property
    def robo_sequencia(self):
        return self._robo_sequencia

    @robo_sequencia.setter
    def robo_sequencia(self, robo_sequencia):
        self._robo_sequencia = robo_sequencia

    @property
    def usuario_robo(self):
        return self._usuario_robo

    @usuario_robo.setter
    def usuario_robo(self, usuario_robo):
        self._usuario_robo = usuario_robo

    def __init__(self, id, nome, descricao, ativo, intervalo, acao, tela, path_executavel, limite_tempo, arquivo_ativacao, nome_executavel, pasta_trabalho, repositorio_planilhas, notificados, pgm_ativado1, pgm_ativado2, robo_sequencia, usuario_robo):
        self._id = id
        self._nome = nome
        self._descricao = descricao
        self._ativo = ativo
        self._intervalo = intervalo
        self._acao = acao
        self._tela = tela
        self._path_executavel = path_executavel
        self._limite_tempo = limite_tempo
        self._arquivo_ativacao = arquivo_ativacao
        self._nome_executavel = nome_executavel
        self._pasta_trabalho = pasta_trabalho
        self._repositorio_planilhas = repositorio_planilhas
        self._notificados = notificados
        self._pgm_ativado1 = pgm_ativado1
        self._pgm_ativado2 = pgm_ativado2
        self._robo_sequencia = robo_sequencia
        self._usuario_robo =usuario_robo



