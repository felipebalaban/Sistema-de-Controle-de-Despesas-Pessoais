import math


class Configuracao:
    """
    Representa as configurações utilizadas pelo sistema.

    Armazena parâmetros configuráveis, como o valor mínimo para
    alertas de alto gasto, o número de meses utilizado em comparativos
    e a meta mensal de economia.
    """
    def __init__(
        self,
        metaMensalEconomia,
        valorMinimoAlerta=500.0,
        mesesComparativo=3
    ):
        self.valorMinimoAlerta = valorMinimoAlerta
        self.mesesComparativo = mesesComparativo
        self.metaMensalEconomia = metaMensalEconomia

    @property
    def valorMinimoAlerta(self):
        return self.__valorMinimoAlerta

    @valorMinimoAlerta.setter
    def valorMinimoAlerta(self, valorMinimoAlerta):
        if not isinstance(valorMinimoAlerta, float):
            raise TypeError("Valor mínimo de alerta deve ser float")

        if not math.isfinite(valorMinimoAlerta):
            raise ValueError("Valor mínimo de alerta deve ser finito")

        if valorMinimoAlerta <= 0:
            raise ValueError("Valor mínimo de alerta deve ser maior que zero")

        self.__valorMinimoAlerta = valorMinimoAlerta

    @property
    def mesesComparativo(self):
        return self.__mesesComparativo

    @mesesComparativo.setter
    def mesesComparativo(self, mesesComparativo):
        if (
            not isinstance(mesesComparativo, int)
            or isinstance(mesesComparativo, bool)
        ):
            raise TypeError("Meses do comparativo devem ser um número inteiro")

        if mesesComparativo <= 0:
            raise ValueError("Meses do comparativo devem ser maiores que zero")

        self.__mesesComparativo = mesesComparativo

    @property
    def metaMensalEconomia(self):
        return self.__metaMensalEconomia

    @metaMensalEconomia.setter
    def metaMensalEconomia(self, metaMensalEconomia):
        if not isinstance(metaMensalEconomia, float):
            raise TypeError("Meta mensal de economia deve ser float")

        if not math.isfinite(metaMensalEconomia):
            raise ValueError("Meta mensal de economia deve ser finita")

        if not 0 <= metaMensalEconomia <= 100:
            raise ValueError("Meta mensal de economia deve estar entre 0 e 100")

        self.__metaMensalEconomia = metaMensalEconomia
