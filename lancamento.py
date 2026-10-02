from datetime import date
from categoria import Categoria
class Lancamento:
    """
    Classe base para representar um lançamento financeiro.

    Serve como base para receitas e despesas, reunindo as
    características comuns aos diferentes tipos de lançamento.
    """
    def __init__(self, valor, data, descricao, categoria, formaDePagamento):
        self.valor = valor
        self.data = data
        self.descricao = descricao
        self.categoria = categoria
        self.formaDePagamento = formaDePagamento

    def __str__(self):
        return f"{self.descricao}: R$ {self.valor:.2f}"

    
    def __repr__(self):
        return (
            f"Lancamento("
            f"valor={self.valor!r}, "
            f"data={self.data!r}, "
            f"descricao={self.descricao!r}, "
            f"categoria={self.categoria!r}, "
            f"formaDePagamento={self.formaDePagamento!r})"
        )

    def __eq__(self, outro):
        if not isinstance(outro, Lancamento):
            return NotImplemented
        return self.data == outro.data and self.descricao == outro.descricao

    def __lt__(self, outro):
        if not isinstance(outro, Lancamento):
            return NotImplemented
        return self.data < outro.data
    
    def __add__(self, outro):
        if type(self) is not type(outro):
            return NotImplemented

        return self.valor + outro.valor


    @property
    def valor(self):
        return self.__valor

    @valor.setter
    def valor(self, valor):
        if not isinstance(valor, float):
            raise TypeError("O valor deve ser float")

        if(valor <= 0):
            raise ValueError("Valor deve ser maior que zero")
        else:
            self.__valor = valor

    @property
    def data(self):
        return self.__data

    @data.setter
    def data(self, data):
        if type(data) is not date:
            raise TypeError("Data deve ser exatamente do tipo date")
        self.__data = data

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TypeError("A descrição precisa ser um string")
        if(len(descricao) > 0):
            self.__descricao = descricao
        else:
            raise ValueError("Descrição não pode ser vazia")

    @property
    def categoria(self):
        return self.__categoria

    @categoria.setter
    def categoria(self, categoria):
        if categoria is not None:
            if not isinstance(categoria, Categoria):
                raise TypeError("Categoria precisa ser um objeto da classe Categoria")
        self.__categoria = categoria

    @property
    def formaDePagamento(self):
        return self.__formaDePagamento

    @formaDePagamento.setter
    def formaDePagamento(self, formaDePagamento):
        if not isinstance(formaDePagamento, str):
            raise TypeError("A forma de pagamento precisa ser string")

        formasPermitidas = ("dinheiro", "debito", "credito", "pix")

        if formaDePagamento not in formasPermitidas:
            raise ValueError("A forma de pagamento precisa ser dinheiro, debito, credito ou pix")
        
        self.__formaDePagamento = formaDePagamento


