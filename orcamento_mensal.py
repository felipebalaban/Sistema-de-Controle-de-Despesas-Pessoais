import math
from receita import Receita
from despesa import Despesa
from datetime import date


class OrcamentoMensal:
    """
    Representa o orçamento financeiro de um determinado mês.

    Agrupa os lançamentos do período e será responsável pelos
    cálculos de receitas, despesas, saldos e limites mensais.
    """
    def __init__(self, mes, ano, receitasPrevistas):
        self.__lancamentos = []
        self.mes = mes
        self.ano = ano
        self.receitasPrevistas = receitasPrevistas


    @property
    def mes(self):
        return self.__mes

    @mes.setter
    def mes(self, mes):
        if not isinstance(mes, int) or isinstance(mes, bool):
            raise TypeError("Mês deve ser um número inteiro")

        if not 1 <= mes <= 12:
            raise ValueError("Mês deve estar entre 1 e 12")

        if self.__lancamentos and mes != self.__mes:
            raise ValueError("Nao é permitido alterar o mes de um orcamento se houverem lancamentos")
        

        self.__mes = mes

    @property
    def ano(self):
        return self.__ano

    @ano.setter
    def ano(self, ano):
        if not isinstance(ano, int) or isinstance(ano, bool):
            raise TypeError("Ano deve ser um número inteiro")

        if not 1 <= ano <= 9999:
            raise ValueError("Ano deve estar entre 1 e 9999")

        if self.__lancamentos and ano != self.__ano:
            raise ValueError(
                "Nao é permitido alterar o ano de um orcamento enquanto houverem lancamentos"
            )

        self.__ano = ano

    @property
    def receitasPrevistas(self):
        return self.__receitasPrevistas

    @receitasPrevistas.setter
    def receitasPrevistas(self, receitasPrevistas):
        if not isinstance(receitasPrevistas, float):
            raise TypeError("Receitas previstas devem ser do tipo float")

        if not math.isfinite(receitasPrevistas):
            raise ValueError("Receitas previstas devem ser um número finito")

        if receitasPrevistas < 0:
            raise ValueError("Receitas previstas não podem ser negativas")

        self.__receitasPrevistas = receitasPrevistas

    @property
    def lancamentos(self):
        return self.__lancamentos.copy()

    def adicionarLancamento(self, lancamento):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise TypeError("Lancamento deve ser uma Receita ou Despesa")

        if (
            lancamento.data.month != self.mes
            or lancamento.data.year != self.ano
        ):
            raise ValueError(
                "A data do lancamento precisa pertencer ao mes e ano do orcamento"

            )

        self.__lancamentos.append(lancamento)

    def removerLancamento(self, lancamento):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise TypeError("Lançamento deve ser uma Receita ou Despesa")

        for indice, lancamentoExistente in enumerate(self.__lancamentos):
            if lancamentoExistente is lancamento:
                del self.__lancamentos[indice]
                return

        raise ValueError("Lançamento não está cadastrado neste orçamento")

    @property
    def totalReceitas(self):
        return self.calcularTotalReceitas()

    @property 
    def totalDespesas(self):
        return self.calcularTotalDespesas()

    @property
    def saldo(self):
        return self.calcularSaldoMensal()

    
    def calcularTotalReceitas(self):
        total = 0.0

        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Receita):
                total += lancamento.valor

        return total

    def calcularTotalDespesas(self):
        total = 0.0

        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                total += lancamento.valor

        return total

    def calcularSaldoMensal(self):
        return self.calcularTotalReceitas() - self.calcularTotalDespesas()

    def calcularSaldoDiario(self, data):
        if type(data) is not date:
            raise TypeError("Data deve ser exatamente do tipo date")

        if data.month != self.mes or data.year != self.ano:
            raise ValueError("A data deve pertencer ao mês e ano do orçamento")

        saldo = 0.0

        for lancamento in self.__lancamentos:
            if lancamento.data <= data:
                if isinstance(lancamento, Receita):
                    saldo += lancamento.valor
                elif isinstance(lancamento, Despesa):
                    saldo -= lancamento.valor

        return saldo

    def verificarDeficit(self):
        return self.calcularSaldoMensal() < 0

    def verificarLimitesCategorias(self):
        totaisPorCategoria = {}

        for lancamento in self.__lancamentos:
            if isinstance(lancamento, Despesa):
                categoria = lancamento.categoria

                if categoria not in totaisPorCategoria:
                    totaisPorCategoria[categoria] = 0.0

                totaisPorCategoria[categoria] += lancamento.valor

        categoriasExcedidas = []

        for categoria, totalGasto in totaisPorCategoria.items():
            if not categoria.validarLimiteMensal(totalGasto):
                categoriasExcedidas.append(categoria)

        return categoriasExcedidas
