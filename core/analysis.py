import pandas as pd
import numpy_financial as npf
from .calculations import calcula_vp_custo_financiamento, calcula_vp_custo_consorcio

def run_scenario_analysis(params: dict) -> pd.DataFrame:
    """
    Executa a análise de sensibilidade com base em variações da taxa de desconto.

    A análise de cenário considera o efeito da mudança de parâmetros-chave
    [cite_start]no resultado de um projeto ou decisão financeira. [cite: 1915]
    """
    base_discount_rate = params['taxa_selic_anual']

    # Define os cenários variando a taxa de desconto (custo de oportunidade)
    scenarios = {
        "Pessimista (Selic Sobe)": base_discount_rate + 0.02,
        "Realista (Selic Atual)": base_discount_rate,
        "Otimista (Selic Cai)": max(0.01, base_discount_rate - 0.02)
    }
    
    results = []
    
    # Recalcula os VPs para cada cenário
    for name, rate in scenarios.items():
        vp_fin = calcula_vp_custo_financiamento(
            valor_entrada=params['valor_entrada'],
            valor_financiado=params['valor_a_financiar'],
            taxa_juros_anual=params['taxa_juros_anual_fin'],
            prazo_meses=params['prazo_meses_fin'],
            taxa_desconto_anual=rate
        )
        
        vp_con = calcula_vp_custo_consorcio(
            parcela=params['parcela_con'],
            prazo=params['prazo_meses_con'],
            taxa_desconto_anual=rate
        )
        
        best_option = "Financiamento" if vp_fin < abs(vp_con) else "Consórcio"
        
        results.append({
            "Cenário": name,
            "Taxa Selic Anual": f"{rate:.2%}",
            "VP Custo Financiamento (R$)": f"{vp_fin:,.2f}",
            "VP Custo Consórcio (R$)": f"{abs(vp_con):,.2f}",
            "Melhor Opção": best_option
        })
        
    return pd.DataFrame(results).set_index("Cenário")


# --- NOVAS FUNÇÕES DE ESTRATÉGIA ---

def simular_estrategia_lance(parcela: float, prazo: int, carta_credito: float, valor_lance_percentual: float, taxa_desconto_anual: float) -> dict:
    """
    Simula o impacto de dar um lance para reduzir o prazo do consórcio.
    Retorna o novo custo em Valor Presente.
    """
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1
    
    valor_do_lance = carta_credito * (valor_lance_percentual / 100)
    parcelas_abatidas = valor_do_lance / parcela
    novo_prazo = round(prazo - parcelas_abatidas)
    
    if novo_prazo <= 0:
        return {'custo_vp': carta_credito, 'novo_prazo': 0}

    fluxo_de_caixa = [-parcela] * novo_prazo
    custo_vp = abs(npf.npv(taxa_desconto_mensal, fluxo_de_caixa))
    
    return {'custo_vp': custo_vp, 'novo_prazo': novo_prazo}


def simular_estrategia_venda(parcela: float, mes_contemplacao: int, agio_venda_percentual: float, taxa_desconto_anual: float) -> dict:
    """
    Simula a venda da cota contemplada como um investimento.
    Retorna o VPL e a TIR da operação. [cite_start]O VPL é o valor presente da sequência de fluxos de caixa [cite: 936][cite_start], e a TIR é a taxa que iguala o VPL a zero. [cite: 1287, 1288]
    """
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1
    
    valor_pago_ate_contemplacao = parcela * mes_contemplacao
    valor_de_venda = valor_pago_ate_contemplacao * (1 + agio_venda_percentual / 100)
    
    # Fluxo de caixa: N saídas (parcelas) e 1 entrada (venda) no final
    fluxo_de_caixa = [-parcela] * mes_contemplacao
    fluxo_de_caixa[-1] += valor_de_venda # A venda acontece no mesmo mês da última parcela paga
    
    vpl = npf.npv(taxa_desconto_mensal, fluxo_de_caixa[1:]) + fluxo_de_caixa[0]
    
    try:
        tir_mensal = npf.irr(fluxo_de_caixa)
        # Anualiza a TIR para melhor interpretação
        tir_anual = (1 + tir_mensal) ** 12 - 1 if tir_mensal is not None else 0
    except:
        tir_anual = 0 # Retorna 0 se a TIR não puder ser calculada

    return {'vpl': vpl, 'tir_anual': tir_anual}


def simular_estrategia_aluguel(parcela: float, prazo: int, mes_contemplacao: int, valor_aluguel: float, taxa_desconto_anual: float) -> dict:
    """
    Simula a estratégia de alugar o bem após a contemplação.
    [cite_start]Retorna o VPL total da operação (custos e receitas). [cite: 936]
    """
    taxa_desconto_mensal = (1 + taxa_desconto_anual)**(1/12) - 1
    
    fluxo_de_caixa = []
    # O primeiro pagamento é no tempo 0 (entrada implícita), mas para simplificar o VPL, consideramos todos a partir do período 1
    for mes in range(1, prazo + 1):
        pagamento = -parcela
        receita_aluguel = 0
        
        if mes > mes_contemplacao:
            receita_aluguel = valor_aluguel
            
        fluxo_de_caixa.append(receita_aluguel + pagamento)
        
    vpl = npf.npv(taxa_desconto_mensal, fluxo_de_caixa)
    
    return {'vpl': vpl}