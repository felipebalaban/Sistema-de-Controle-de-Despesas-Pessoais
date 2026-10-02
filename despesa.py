from lancamento import Lancamento
from categoria import Categoria

class Despesa(Lancamento):
    """
    Representa um lançamento financeiro do tipo despesa.

    Herda de Lancamento as características comuns aos lançamentos
    e será responsável pelas regras específicas relacionadas
    às despesas.
    """

    

    def verificarAltoValor(self, limite = 500.0):
        return self.valor > limite

    @Lancamento.categoria.setter
    def categoria(self, categoria):
        if categoria is None:
            raise ValueError("A despesa precisa ter uma categoria")

        if not isinstance(categoria, Categoria):
            raise TypeError("Categoria precisa ser um objeto da classe Categoria")

        if categoria.tipo != "despesa":
            raise ValueError("Despesa precisa de uma categoria do tipo despesa")

        Lancamento.categoria.fset(self, categoria)
                