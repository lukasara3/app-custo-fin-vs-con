import pandas as pd
from .calculations import calcula_vp_custo_financiamento, calcula_vp_custo_consorcio

def run_scenario_analysis(params: dict) -> pd.DataFrame:
    """
    Executa a análise de sensibilidade com base em variações da taxa de desconto.

    A análise de cenário considera o efeito da mudança de parâmetros-chave
    [cite_start]no resultado de um projeto ou decisão financeira. [cite: 2484]

    Args:
        params (dict): Um dicionário contendo todos os inputs necessários para os cálculos.

    Returns:
        pd.DataFrame: Uma tabela com os resultados para cada cenário.
    """
    base_discount_rate = params['taxa_selic_anual']

    # Define os cenários variando a taxa de desconto (custo de oportunidade)
    scenarios = {
        "Pessimista (Selic Sobe)": base_discount_rate + 0.02,  # Selic +2 p.p.
        "Realista (Selic Atual)": base_discount_rate,
        "Otimista (Selic Cai)": max(0.01, base_discount_rate - 0.02)  # Selic -2 p.p., com mínimo de 1%
    }
    
    results = []
    
    # Recalcula os VPs para cada cenário
    for name, rate in scenarios.items():
        vp_fin = calcula_vp_custo_financiamento(
            valor_entrada=params['valor_entrada'],
            valor_financiado=params['valor_a_financiar'],
            taxa_juros_anual=params['taxa_juros_anual_fin'],
            prazo_meses=params['prazo_meses_fin'],
            taxa_desconto_anual=rate  # Usa a taxa do cenário
        )
        
        vp_con = calcula_vp_custo_consorcio(
            parcela=params['parcela_con'],
            prazo=params['prazo_meses_con'],
            taxa_desconto_anual=rate  # Usa a taxa do cenário
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