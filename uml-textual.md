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
- `despesasPorCategoria()`
- `despesasPorFormaPagamento()`
- `percentualPorCategoria()`
- `mesMaisEconomico()`
- `compararMeses()`

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

**Atributos:** nenhum.

**Métodos:**
- `adicionarCategoria()`
- `editarCategoria()`
- `excluirCategoria()`
- `adicionarLancamento()`
- `editarLancamento()`
- `excluirLancamento()`