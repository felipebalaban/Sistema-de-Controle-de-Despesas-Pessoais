from datetime import date
class Alerta:
    """
    Representa uma notificação gerada pelas regras do sistema.

    É utilizada para registrar situações como despesas de alto valor,
    limites de categoria excedidos e déficit orçamentário.
    """
    def __init__(self, tipo, mensagem, data):
        self.tipo = tipo
        self.mensagem = mensagem
        self.data = data

    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo, str):
            raise TypeError("Tipo do alerta deve ser um string")

        tiposPermitidos = (
            "altoValor",
            "limiteExcedido",
            "deficitOrcamentario"
        )

        if tipo not in tiposPermitidos:
            raise ValueError("Tipo deve ser alto valor, limite excedido ou déficit orçamentário")

        self.__tipo = tipo

    @property
    def mensagem(self):
        return self.__mensagem

    @mensagem.setter
    def mensagem(self, mensagem):
        if not isinstance(mensagem, str):
            raise TypeError("Mensagem deve ser uma string")

        if not mensagem.strip():
            raise ValueError("Mensagem não pode ser vazia ou conter apenas espaços")

        self.__mensagem = mensagem

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if type(data) is not date:
            raise TypeError("Data deve ser exatamente do tipo date")

        self.__data = data