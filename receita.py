from lancamento import Lancamento
from categoria import Categoria

class Receita(Lancamento):
    """
    Representa um lançamento financeiro do tipo receita.

    Herda de Lancamento as características comuns aos
    lançamentos financeiros.
    """


    @Lancamento.categoria.setter
    def categoria(self, categoria):
        if categoria is not None:
            if not isinstance(categoria, Categoria):
                raise TypeError("Categoria precisa ser um objeto da classe Categoria")

            if categoria.tipo != "receita":
                raise ValueError("Receita precisa de uma categoria do tipo receita")
        Lancamento.categoria.fset(self, categoria)