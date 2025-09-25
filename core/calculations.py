import numpy_financial as npf
import pandas as pd

# Financiamento


# Consórcio
def calcula_parcela_consorcio(carta_credito: float, prazo: int, tx_adm: float, fundo_reserva: float = 0.0) -> float:
    """
    Calcula o valor da parcela mensal de um consórcio.

    Args:
        carta_credito (float): O valor total da carta de crédito.
        prazo (int): O número total de meses do plano.
        tx_adm (float): A taxa de administração total do período (em percentual, ex: 15 para 15%).
        fundo_reserva (float, optional): A taxa do fundo de reserva total (em percentual, ex: 2 para 2%). Default é 0.

    Returns:
        float: O valor da parcela mensal.
    """
    if prazo <= 0:
        raise ValueError("O prazo deve ser um número positivo de meses.")

    # Converte as taxas de percentual para decimal
    tx_adm_decimal = tx_adm / 100
    fr_decimal = fundo_reserva / 100

    # O valor total a ser pago é a carta de crédito mais as taxas
    valor_total_pago = carta_credito * (1 + tx_adm_decimal + fr_decimal)

    parcela_mensal = valor_total_pago / prazo
    
    return parcela_mensal


def calcula_vp_custo_consorcio(parcela: float, prazo: int, taxa_desconto_anual: float) -> float:
    """
    Calcula o Valor Presente (VP) do custo total de um consórcio.
    Isso representa o "custo real" do consórcio em dinheiro de hoje.

    Args:
        parcela (float): O valor da parcela mensal.
        prazo (int): O número total de meses do plano.
        taxa_desconto_anual (float): A taxa de desconto anual (ex: Selic) para trazer os pagamentos a valor presente.
                                     Fornecida em decimal (ex: 0.1 para 10%).

    Returns:
        float: O valor presente do fluxo de pagamentos (será um valor negativo, pois é um custo).
    """
    if prazo <= 0:
        return 0.0

    # Converte a taxa de desconto anual para mensal, pois os pagamentos são mensais
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1

    # Cria uma lista com todos os pagamentos (fluxo de caixa negativo)
    fluxo_de_caixa = [-parcela] * prazo
    
    # Calcula o Valor Presente Líquido (VPL) do fluxo de caixa
    # No nosso caso, como não há investimento inicial no tempo 0, o VPL é o VP dos custos.
    valor_presente = npf.npv(taxa_desconto_mensal, fluxo_de_caixa)
    
    return valor_presente