class Categoria:
    """
    Representa uma categoria utilizada para classificar lançamentos.

    Uma categoria pode ser do tipo receita ou despesa e, no caso
    de despesas, pode possuir um limite mensal de gastos.
    """
    #nome, descricao, tipo (receita ou despesa) e limiteMensal e validarLimiteMensal()

    def __init__(self, nome, descricao, tipo, limiteMensal):
        self.nome = nome;
        self.descricao = descricao;
        self.tipo = tipo;
        self.limiteMensal = limiteMensal
        

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome precisa ser string")
        if(len(nome) >0):
            self.__nome = nome
        else:
            raise ValueError("O nome não pode ser vazio")

        

    @property
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao):
        if not isinstance(descricao, str):
            raise TypeError("A descrição precisa ser um string")
            
        self.__descricao = descricao


    @property
    def tipo(self):
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo):
        if not isinstance(tipo, str):
            raise TypeError("O tipo precisa ser uma string")

        tiposPermitidos = ("receita", "despesa")

        if tipo not in tiposPermitidos:
            raise ValueError("O tipo deve ser receita ou despesa")

        if tipo == "receita" and getattr(self, "_Categoria__limiteMensal", None) is not None:
            raise ValueError("Você precisa remover o limite mensal antes de alterar o tipo para receita")
        

        self.__tipo = tipo


    @property
    def limiteMensal(self):
        return self.__limiteMensal

    @limiteMensal.setter
    def limiteMensal(self, limiteMensal):
        if limiteMensal is None:
            self.__limiteMensal = None
            return
        if not isinstance(limiteMensal, float):
            raise TypeError("O limite deve ser float ou None")
        if self.tipo == "receita":
            raise ValueError("Categorias de receita não podem ter limite")
        if limiteMensal <= 0:
            raise ValueError("O limite deve ser maior que zero")

        self.__limiteMensal = limiteMensal

    def validarLimiteMensal(self, totalGasto):
        if not isinstance(totalGasto, (int, float)) or isinstance(totalGasto, bool):
            raise TypeError("O total gasto precisa ser um número")
        if totalGasto < 0:
            raise ValueError("Total gasto nao pode ser negativo")
        if self.limiteMensal is None:
            return True

        return totalGasto <= self.limiteMensal