from datetime import date

from configuracao import Configuracao
from categoria import Categoria
from orcamento_mensal import OrcamentoMensal
from alerta import Alerta
from receita import Receita
from despesa import Despesa

class GerenciadorFinanceiro:
    """
    Responsável por coordenar as principais operações do sistema.

    Gerencia o cadastro, a edição e a exclusão de categorias e
    lançamentos.
    """
    def __init__(self, configuracao):
        self.configuracao = configuracao
        self.__categorias = []
        self.__orcamentos = []
        self.__alertas = []

    @property
    def configuracao(self):
        return self.__configuracao

    @configuracao.setter
    def configuracao(self, configuracao):
        if not isinstance(configuracao, Configuracao):
            raise TypeError(
                "Configuração deve ser um objeto da classe Configuracao"
            )

        self.__configuracao = configuracao

    @property
    def categorias(self):
        return self.__categorias.copy()

    @property
    def orcamentos(self):
        return self.__orcamentos.copy()

    @property
    def alertas(self):
        return self.__alertas.copy()

    def adicionarAlerta(self, alerta):
        if not isinstance(alerta, Alerta):
            raise TypeError("Alerta deve ser um objeto da classe Alerta")

        self.__alertas.append(alerta)

    def adicionarOrcamento(self, orcamento):
        if not isinstance(orcamento, OrcamentoMensal):
            raise TypeError("Orçamento deve ser um objeto da classe OrcamentoMensal")

        for orcamentoExistente in self.__orcamentos:
            if (
                orcamentoExistente.mes == orcamento.mes
                and orcamentoExistente.ano == orcamento.ano
            ):
                raise ValueError("Já existe um orçamento para esse mês e ano")

        self.__orcamentos.append(orcamento)

    def adicionarCategoria(self, categoria):
        if not isinstance(categoria, Categoria):
            raise TypeError("Categoria deve ser um objeto da classe Categoria")

        for categoriaExistente in self.__categorias:
            if (
                categoriaExistente.nome == categoria.nome
                and categoriaExistente.tipo == categoria.tipo
            ):
                raise ValueError("Já existe uma categoria com esse nome e tipo")

        self.__categorias.append(categoria)

    def editarCategoria(self, categoria, nome, descricao, tipo, limiteMensal):
        if not isinstance(categoria, Categoria):
            raise TypeError("Categoria deve ser um objeto da classe Categoria")

        encontrada = False

        for categoriaExistente in self.__categorias:
            if categoriaExistente is categoria:
                encontrada = True
                break

        if not encontrada:
            raise ValueError("Categoria não está cadastrada")

        novosDados = Categoria(nome, descricao, tipo, limiteMensal)

        for categoriaExistente in self.__categorias:
            if (
                categoriaExistente is not categoria
                and categoriaExistente.nome == novosDados.nome
                and categoriaExistente.tipo == novosDados.tipo
            ):
                raise ValueError("Já existe uma categoria com esse nome e tipo")

        if categoria.tipo != novosDados.tipo:
            for orcamento in self.__orcamentos:
                for lancamento in orcamento.lancamentos:
                    if lancamento.categoria is categoria:
                        raise ValueError(
                            "Não é possível alterar o tipo de uma categoria "
                            "com lançamentos vinculados"
                        )

        categoria.limiteMensal = None
        categoria.tipo = novosDados.tipo
        categoria.limiteMensal = novosDados.limiteMensal
        categoria.nome = novosDados.nome
        categoria.descricao = novosDados.descricao

    def excluirCategoria(self, categoria):
        if not isinstance(categoria, Categoria):
            raise TypeError("Categoria deve ser um objeto da classe Categoria")

        encontrada = False

        for categoriaExistente in self.__categorias:
            if categoriaExistente is categoria:
                encontrada = True
                break

        if not encontrada:
            raise ValueError("Categoria não está cadastrada")

        for orcamento in self.__orcamentos:
            for lancamento in orcamento.lancamentos:
                if lancamento.categoria is categoria:
                    raise ValueError(
                        "Não é possível excluir uma categoria "
                        "com lançamentos vinculados"
                    )

        self.__categorias.remove(categoria)

    def adicionarLancamento(self, lancamento):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise TypeError("Lançamento deve ser uma Receita ou Despesa")

        if lancamento.categoria is not None:
            categoriaEncontrada = False

            for categoria in self.__categorias:
                if categoria is lancamento.categoria:
                    categoriaEncontrada = True
                    break

            if not categoriaEncontrada:
                raise ValueError("A categoria do lançamento não está cadastrada")

        for orcamento in self.__orcamentos:
            for lancamentoExistente in orcamento.lancamentos:
                if lancamentoExistente is lancamento:
                    raise ValueError("Esse lançamento já foi adicionado")

        for orcamento in self.__orcamentos:
            if (
                orcamento.mes == lancamento.data.month
                and orcamento.ano == lancamento.data.year
            ):
                deficitAntes = orcamento.verificarDeficit()
                categoriasExcedidasAntes = orcamento.verificarLimitesCategorias()

                orcamento.adicionarLancamento(lancamento)

                dataAlerta = date.today()

                if isinstance(lancamento, Despesa):
                    if lancamento.verificarAltoValor(
                        self.configuracao.valorMinimoAlerta
                    ):
                        alerta = Alerta(
                            "altoValor",
                            f"Despesa '{lancamento.descricao}' de "
                            f"R$ {lancamento.valor:.2f} ultrapassou o valor "
                            f"de alerta configurado.",
                            dataAlerta
                        )
                        self.adicionarAlerta(alerta)

                categoriasExcedidasDepois = orcamento.verificarLimitesCategorias()

                for categoria in categoriasExcedidasDepois:
                    if categoria not in categoriasExcedidasAntes:
                        alerta = Alerta(
                            "limiteExcedido",
                            f"A categoria '{categoria.nome}' ultrapassou "
                            f"seu limite em {orcamento.mes:02d}/{orcamento.ano}.",
                            dataAlerta
                        )
                        self.adicionarAlerta(alerta)

                if not deficitAntes and orcamento.verificarDeficit():
                    alerta = Alerta(
                        "deficitOrcamentario",
                        f"O orçamento de {orcamento.mes:02d}/{orcamento.ano} "
                        f"ficou negativo. Saldo: R$ {orcamento.saldo:.2f}.",
                        dataAlerta
                    )
                    self.adicionarAlerta(alerta)

                return

        raise ValueError("Não existe orçamento cadastrado para o mês e ano do lançamento")

    def editarLancamento(
        self, lancamento, valor, data, descricao, categoria, formaDePagamento
    ):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise TypeError("Lançamento deve ser uma Receita ou Despesa")

        orcamentoOrigem = None

        for orcamento in self.__orcamentos:
            for lancamentoExistente in orcamento.lancamentos:
                if lancamentoExistente is lancamento:
                    orcamentoOrigem = orcamento
                    break
            if orcamentoOrigem is not None:
                break

        if orcamentoOrigem is None:
            raise ValueError("Lançamento não está cadastrado no gerenciador")

        novosDados = type(lancamento)(
            valor, data, descricao, categoria, formaDePagamento
        )

        if novosDados.categoria is not None:
            categoriaEncontrada = False
            for categoriaExistente in self.__categorias:
                if categoriaExistente is novosDados.categoria:
                    categoriaEncontrada = True
                    break
            if not categoriaEncontrada:
                raise ValueError("A categoria do lançamento não está cadastrada")

        orcamentoDestino = None

        for orcamento in self.__orcamentos:
            if (
                orcamento.mes == novosDados.data.month
                and orcamento.ano == novosDados.data.year
            ):
                orcamentoDestino = orcamento
                break

        if orcamentoDestino is None:
            raise ValueError("Não existe orçamento cadastrado para o mês e ano do lançamento")

        orcamentosAfetados = [orcamentoOrigem]
        if orcamentoDestino is not orcamentoOrigem:
            orcamentosAfetados.append(orcamentoDestino)

        situacoesAntes = []
        for orcamento in orcamentosAfetados:
            situacoesAntes.append((
                orcamento,
                orcamento.verificarDeficit(),
                orcamento.verificarLimitesCategorias()
            ))

        altoValorAntes = False
        if isinstance(lancamento, Despesa):
            altoValorAntes = lancamento.verificarAltoValor(
                self.configuracao.valorMinimoAlerta
            )

        if orcamentoDestino is not orcamentoOrigem:
            orcamentoOrigem.removerLancamento(lancamento)

        lancamento.valor = novosDados.valor
        lancamento.data = novosDados.data
        lancamento.descricao = novosDados.descricao
        lancamento.categoria = novosDados.categoria
        lancamento.formaDePagamento = novosDados.formaDePagamento

        if orcamentoDestino is not orcamentoOrigem:
            orcamentoDestino.adicionarLancamento(lancamento)

        dataAlerta = date.today()

        if isinstance(lancamento, Despesa):
            if not altoValorAntes and lancamento.verificarAltoValor(
                self.configuracao.valorMinimoAlerta
            ):
                self.adicionarAlerta(Alerta(
                    "altoValor",
                    f"Despesa '{lancamento.descricao}' de "
                    f"R$ {lancamento.valor:.2f} ultrapassou o valor "
                    f"de alerta configurado após a edição.",
                    dataAlerta
                ))

        for orcamento, deficitAntes, categoriasExcedidasAntes in situacoesAntes:
            for categoriaExcedida in orcamento.verificarLimitesCategorias():
                if categoriaExcedida not in categoriasExcedidasAntes:
                    self.adicionarAlerta(Alerta(
                        "limiteExcedido",
                        f"A categoria '{categoriaExcedida.nome}' ultrapassou "
                        f"seu limite em {orcamento.mes:02d}/{orcamento.ano} "
                        f"após a edição de um lançamento.",
                        dataAlerta
                    ))

            if not deficitAntes and orcamento.verificarDeficit():
                self.adicionarAlerta(Alerta(
                    "deficitOrcamentario",
                    f"O orçamento de {orcamento.mes:02d}/{orcamento.ano} "
                    f"ficou negativo após a edição de um lançamento. "
                    f"Saldo: R$ {orcamento.saldo:.2f}.",
                    dataAlerta
                ))

    def excluirLancamento(self, lancamento):
        if not isinstance(lancamento, (Receita, Despesa)):
            raise TypeError("Lançamento deve ser uma Receita ou Despesa")

        for orcamento in self.__orcamentos:
            for lancamentoExistente in orcamento.lancamentos:
                if lancamentoExistente is lancamento:
                    deficitAntes = orcamento.verificarDeficit()

                    orcamento.removerLancamento(lancamento)

                    if not deficitAntes and orcamento.verificarDeficit():
                        alerta = Alerta(
                            "deficitOrcamentario",
                            f"O orçamento de {orcamento.mes:02d}/{orcamento.ano} "
                            f"ficou negativo após a exclusão de um lançamento. "
                            f"Saldo: R$ {orcamento.saldo:.2f}.",
                            date.today()
                        )
                        self.adicionarAlerta(alerta)

                    return

        raise ValueError("Lançamento não está cadastrado no gerenciador")
