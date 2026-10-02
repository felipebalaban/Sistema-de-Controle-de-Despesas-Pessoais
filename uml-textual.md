# UML Textual

## Classe Lancamento

**Atributos:**
- `valor`
- `data`
- `descrição`
- `categoria`
- `formaDePagamento`

**Métodos:**
- `__str__()`
- `__repr__()`
- `__eq__()`
- `__lt__()`
- `__add__()`

## Classe Receita

Herda de `Lancamento`.

**Atributos adicionais:** nenhum.

**Métodos adicionais:** nenhum.

## Classe Despesa

Herda de `Lancamento`.

**Atributos adicionais:** nenhum.

**Métodos:**
- `verificarAltoValor()`

## Classe Categoria

**Atributos:**
- `nome`
- `descrição`
- `tipo` (receita ou despesa)
- `limiteMensal`

**Métodos:**
- `validarLimiteMensal()`

## Classe OrcamentoMensal

**Atributos:**
- `mes`
- `ano`
- `receitasPrevistas`
- `lancamentos`
- `totalReceitas`
- `totalDespesas`
- `saldo`

**Métodos:**
- `adicionarLancamento()`
- `removerLancamento()`
- `calcularTotalReceitas()`
- `calcularTotalDespesas()`
- `calcularSaldoMensal()`
- `calcularSaldoDiario(data)`
- `verificarDeficit()`
- `verificarLimitesCategorias()`

## Classe Alerta

**Atributos:**
- `tipo`
- `mensagem`
- `data`

**Métodos:** nenhum.

## Classe Relatorio

**Atributos:** nenhum.

**Métodos:**
- `despesasPorCategoria(orcamento)` — totais por objeto `Categoria`.
- `despesasPorFormaPagamento(orcamento)` — listas de despesas por forma de pagamento.
- `percentualPorCategoria(orcamento)` — percentuais de 0 a 100; vazio quando não há despesas.
- `mesMaisEconomico(orcamentos)` — orçamento com menor total de despesas; empate pelo mês mais antigo; `None` para lista vazia.
- `compararMeses(orcamentos, mesesComparativo=3, dataReferencia=None)` — receitas, despesas e saldo em ordem cronológica, incluindo o mês de referência (atual por padrão) e os anteriores; meses sem orçamento são omitidos. Aceita `configuracao.mesesComparativo` como quantidade de meses.

Os relatórios não alteram os dados recebidos. Categorias compartilhadas são agrupadas pelo mesmo objeto. Coleções de orçamentos não podem repetir mês e ano.

## Classe Configuracao

**Atributos:**
- `valorMinimoAlerta`
- `mesesComparativo`
- `metaMensalEconomia`

**Métodos:** nenhum.

## Classe Repositorio

**Atributos:** nenhum.

**Métodos:**
- `salvarLancamentos()`
- `carregarLancamentos()`
- `salvarCategorias()`
- `carregarCategorias()`
- `salvarOrcamentos()`
- `carregarOrcamentos()`

## Classe GerenciadorFinanceiro

**Atributos:**
- `categorias`
- `orcamentos`
- `alertas`
- `configuracao`

**Métodos:**
- `adicionarCategoria()`
- `editarCategoria()`
- `excluirCategoria()`
- `adicionarOrcamento()`
- `adicionarAlerta()`
- `adicionarLancamento()`
- `editarLancamento()`
- `excluirLancamento()`
