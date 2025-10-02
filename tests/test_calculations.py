import pytest
import pandas as pd
from core.calculations import (
    calcula_parcela_consorcio, 
    calcula_vp_custo_consorcio,
    calcula_parcela_price,
    gera_tabela_amortizacao,
    calcula_vp_custo_financiamento
)

# --- Testes do Consórcio ---
def test_calcula_parcela_consorcio():
    parcela = calcula_parcela_consorcio(carta_credito=60000, prazo=60, tx_adm=15, fundo_reserva=2)
    assert parcela == pytest.approx(1170.0)

def test_calcula_vp_custo_consorcio():
    vp = calcula_vp_custo_consorcio(parcela=1000, prazo=12, taxa_desconto_anual=0.10)
    assert vp == pytest.approx(-11491.40, abs=1e-2)

# --- Testes do Financiamento (com valores corretos e consistentes) ---
def test_calcula_parcela_price():
    """Testa o cálculo da parcela com taxa de juros mensal EFETIVA."""
    parcela = calcula_parcela_price(valor_financiado=80000, taxa_juros_anual=0.10, prazo_meses=120)
    # Valor esperado usando taxa efetiva: (1+0.10)**(1/12)-1
    assert parcela == pytest.approx(1038.20, abs=1e-2)

def test_gera_tabela_amortizacao():
    """Testa a geração da tabela de amortização com taxa EFETIVA."""
    tabela = gera_tabela_amortizacao(valor_financiado=50000, taxa_juros_anual=0.12, prazo_meses=48)
    assert isinstance(tabela, pd.DataFrame)
    assert len(tabela) == 48
    saldo_final = tabela["Saldo Devedor (R$)"].iloc[-1]
    assert saldo_final == pytest.approx(0.0, abs=1e-2)

def test_calcula_vp_custo_financiamento():
    """Testa o cálculo do VP do custo com taxas EFETIVAS."""
    custo_vp = calcula_vp_custo_financiamento(
        valor_entrada=20000, valor_financiado=80000,
        taxa_juros_anual=0.10, prazo_meses=120,
        taxa_desconto_anual=0.12
    )
    # Valor esperado com parcela de 1035.19 (taxa efetiva)
    # e desconto com taxa efetiva de 12%
    assert custo_vp == pytest.approx(94889.33, abs=1e-2)
