import numpy_financial as npf
import pandas as pd

# --- FUNÇÕES DE FINANCIAMENTO ---

def calcula_parcela_price(valor_financiado: float, taxa_juros_anual: float, prazo_meses: int) -> float:
    """Calcula o valor da parcela fixa (PMT) para um financiamento pelo sistema Price."""
    if prazo_meses <= 0:
        return 0.0
    # PADRONIZAÇÃO: Usa a taxa de juros mensal EFETIVA
    taxa_juros_mensal = (1 + taxa_juros_anual)**(1/12) - 1
    parcela = npf.pmt(rate=taxa_juros_mensal, nper=prazo_meses, pv=-valor_financiado)
    return parcela

def gera_tabela_amortizacao(valor_financiado: float, taxa_juros_anual: float, prazo_meses: int) -> pd.DataFrame:
    """Gera uma tabela de amortização completa para um financiamento pelo sistema Price."""
    # PADRONIZAÇÃO: Usa a taxa de juros mensal EFETIVA
    taxa_juros_mensal = (1 + taxa_juros_anual)**(1/12) - 1
    parcela = calcula_parcela_price(valor_financiado, taxa_juros_anual, prazo_meses)
    
    saldo_devedor = valor_financiado
    dados_tabela = []
    for mes in range(1, prazo_meses + 1):
        juros_periodo = saldo_devedor * taxa_juros_mensal
        amortizacao = parcela - juros_periodo
        saldo_devedor -= amortizacao
        if mes == prazo_meses:
            saldo_devedor = 0.0
        dados_tabela.append({
            "Mês": mes, "Parcela (R$)": parcela, "Juros (R$)": juros_periodo,
            "Amortização (R$)": amortizacao, "Saldo Devedor (R$)": saldo_devedor
        })
    return pd.DataFrame(dados_tabela)

def calcula_vp_custo_financiamento(valor_entrada: float, valor_financiado: float, taxa_juros_anual: float, prazo_meses: int, taxa_desconto_anual: float) -> float:
    """Calcula o custo total de um financiamento em Valor Presente (VP)."""
    parcela = calcula_parcela_price(valor_financiado, taxa_juros_anual, prazo_meses)
    
    # PADRONIZAÇÃO: Usa a taxa de desconto mensal EFETIVA
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1
    
    fluxo_parcelas = [-parcela] * prazo_meses
    vp_das_parcelas = npf.npv(rate=taxa_desconto_mensal, values=fluxo_parcelas)
    
    custo_total_vp = valor_entrada + abs(vp_das_parcelas)
    return custo_total_vp

# --- FUNÇÕES DE CONSÓRCIO ---

def calcula_parcela_consorcio(carta_credito: float, prazo: int, tx_adm: float, fundo_reserva: float = 0.0) -> float:
    """Calcula o valor da parcela mensal de um consórcio."""
    if prazo <= 0:
        raise ValueError("O prazo deve ser um número positivo de meses.")
    tx_adm_decimal = tx_adm / 100
    fr_decimal = fundo_reserva / 100
    valor_total_pago = carta_credito * (1 + tx_adm_decimal + fr_decimal)
    parcela_mensal = valor_total_pago / prazo
    return parcela_mensal

def calcula_vp_custo_consorcio(parcela: float, prazo: int, taxa_desconto_anual: float) -> float:
    """Calcula o Valor Presente (VP) do custo total de um consórcio."""
    if prazo <= 0:
        return 0.0
    # PADRONIZAÇÃO: Usa a taxa de desconto mensal EFETIVA
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1
    fluxo_de_caixa = [-parcela] * prazo
    valor_presente = npf.npv(taxa_desconto_mensal, fluxo_de_caixa)
    return valor_presente