from datetime import date

from despesa import Despesa
from orcamento_mensal import OrcamentoMensal


class Relatorio:
    """
    Representa os relatórios e estatísticas financeiras do sistema.

    Será responsável por analisar lançamentos e orçamentos para
    apresentar informações como despesas por categoria, despesas por
    forma de pagamento, percentuais, comparações entre meses e o mês
    com menor total de despesas.
    """
    def despesasPorCategoria(self, orcamento):
        """Retorna um dicionário de objetos Categoria para totais de despesas."""
        if not isinstance(orcamento, OrcamentoMensal):
            raise TypeError("Orçamento deve ser um objeto OrcamentoMensal")

        totais = {}
        for lancamento in orcamento.lancamentos:
            if isinstance(lancamento, Despesa):
                categoria = lancamento.categoria
                if categoria not in totais:
                    totais[categoria] = 0.0
                totais[categoria] += lancamento.valor

        return totais

    def despesasPorFormaPagamento(self, orcamento):
        """Retorna listas de despesas agrupadas pelas formas de pagamento usadas."""
        if not isinstance(orcamento, OrcamentoMensal):
            raise TypeError("Orçamento deve ser um objeto OrcamentoMensal")

        grupos = {}
        for lancamento in orcamento.lancamentos:
            if isinstance(lancamento, Despesa):
                forma = lancamento.formaDePagamento
                if forma not in grupos:
                    grupos[forma] = []
                grupos[forma].append(lancamento)

        return grupos

    def percentualPorCategoria(self, orcamento):
        """Retorna percentuais de 0 a 100; sem despesas, retorna {}."""
        totais = self.despesasPorCategoria(orcamento)
        totalDespesas = sum(totais.values())
        percentuais = {}

        if totalDespesas == 0:
            return percentuais

        for categoria, total in totais.items():
            percentuais[categoria] = total / totalDespesas * 100

        return percentuais

    def mesMaisEconomico(self, orcamentos):
        """Retorna o orçamento com menos despesas; em empate, o mais antigo.

        Uma coleção vazia retorna None. Orçamentos cadastrados sem despesas
        participam com total zero, independentemente das receitas.
        """
        self.__validarOrcamentos(orcamentos)
        maisEconomico = None

        for orcamento in orcamentos:
            if maisEconomico is None or (
                orcamento.totalDespesas, orcamento.ano, orcamento.mes
            ) < (
                maisEconomico.totalDespesas, maisEconomico.ano, maisEconomico.mes
            ):
                maisEconomico = orcamento

        return maisEconomico

    def compararMeses(self, orcamentos, mesesComparativo=3, dataReferencia=None):
        """Retorna resumos cronológicos dos orçamentos dentro da janela mensal.

        A janela inclui o mês de dataReferencia (hoje, por padrão) e os meses
        anteriores. Meses sem orçamento são omitidos, sem inventar totais zero.
        Pode receber configuracao.mesesComparativo como segundo argumento.
        """
        self.__validarOrcamentos(orcamentos)
        if not isinstance(mesesComparativo, int) or isinstance(mesesComparativo, bool):
            raise TypeError("Meses do comparativo devem ser um número inteiro")
        if mesesComparativo <= 0:
            raise ValueError("Meses do comparativo devem ser maiores que zero")

        if dataReferencia is None:
            dataReferencia = date.today()
        if type(dataReferencia) is not date:
            raise TypeError("Data de referência deve ser exatamente do tipo date")

        mesFinal = (dataReferencia.year - 1) * 12 + dataReferencia.month - 1
        mesInicial = mesFinal - mesesComparativo + 1
        comparativo = []

        for orcamento in sorted(orcamentos, key=lambda item: (item.ano, item.mes)):
            mesOrcamento = (orcamento.ano - 1) * 12 + orcamento.mes - 1
            if mesInicial <= mesOrcamento <= mesFinal:
                receitas = orcamento.totalReceitas
                despesas = orcamento.totalDespesas
                comparativo.append({
                    "mes": orcamento.mes,
                    "ano": orcamento.ano,
                    "totalReceitas": receitas,
                    "totalDespesas": despesas,
                    "saldo": receitas - despesas
                })

        return comparativo

    def __validarOrcamentos(self, orcamentos):
        if not isinstance(orcamentos, (list, tuple)):
            raise TypeError("Orçamentos devem ser fornecidos em uma lista ou tupla")

        periodos = set()
        for orcamento in orcamentos:
            if not isinstance(orcamento, OrcamentoMensal):
                raise TypeError("Cada orçamento deve ser um objeto OrcamentoMensal")
            periodo = (orcamento.ano, orcamento.mes)
            if periodo in periodos:
                raise ValueError("Há mais de um orçamento para o mesmo mês e ano")
            periodos.add(periodo)
