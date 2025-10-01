import streamlit as st
import pandas as pd
# Importe as funções que vocês criaram no módulo de cálculos
from core.calculations import (
    calcula_parcela_price,
    gera_tabela_amortizacao,
    calcula_vp_custo_financiamento,
    calcula_parcela_consorcio,
    calcula_vp_custo_consorcio
)
# A Pessoa B irá criar esta função. Por enquanto, a linha abaixo pode dar erro até o arquivo existir.
from core.data_fetcher import busca_taxa_selic_atual

# --- Configuração da Página ---
st.set_page_config(
    page_title="Calculadora Estratégica",
    page_icon="💰",
    layout="wide"
)

st.title("Calculadora Estratégica: Financiamento vs. Consórcio")
st.markdown("Uma ferramenta para análise do custo efetivo de aquisição de bens, baseada no Valor do Dinheiro no Tempo.")

# --- Barra Lateral para Inputs do Usuário ---
st.sidebar.header("Parâmetros de Entrada")

# --- Busca de Dados e Inputs Gerais ---
# Esta função será criada pela Pessoa B. Ela busca a Selic real e permite que o usuário a ajuste.
selic_atual = busca_taxa_selic_atual()
taxa_selic_anual = st.sidebar.slider(
    "Taxa de Oportunidade (Selic Anual %)", 
    min_value=1.0, 
    max_value=20.0, 
    value=selic_atual * 100, # O valor padrão agora é o valor real da API
    step=0.25
) / 100
st.sidebar.caption(f"Taxa Selic Meta atual: {selic_atual*100:.2f}% a.a.")

valor_bem = st.sidebar.number_input("Valor do Bem (R$)", min_value=1000, value=300000, step=5000)

# --- Inputs do Financiamento ---
with st.sidebar.expander("Dados do Financiamento", expanded=True):
    valor_entrada = st.sidebar.number_input("Valor da Entrada (R$)", min_value=0, value=60000, step=1000)
    taxa_juros_anual_fin = st.sidebar.slider("Taxa de Juros do Financiamento Anual (%)", min_value=1.0, max_value=25.0, value=11.5, step=0.25) / 100
    prazo_meses_fin = st.sidebar.slider("Prazo do Financiamento (meses)", min_value=12, max_value=420, value=360, step=12)

# --- Inputs do Consórcio ---
with st.sidebar.expander("Dados do Consórcio", expanded=True):
    prazo_meses_con = st.sidebar.slider("Prazo do Grupo do Consórcio (meses)", min_value=12, max_value=240, value=180, step=12)
    taxa_adm_total = st.sidebar.slider("Taxa de Administração Total (%)", min_value=5.0, max_value=30.0, value=18.0, step=0.5)
    fundo_reserva_total = st.sidebar.slider("Fundo de Reserva Total (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.25)

# --- Botão para Executar os Cálculos ---
if st.sidebar.button("Analisar", type="primary", use_container_width=True):
    
    # Validação da entrada
    if valor_entrada >= valor_bem:
        st.error("O valor da entrada não pode ser maior ou igual ao valor do bem.")
    else:
        # 1. Cálculos do Financiamento
        valor_a_financiar = valor_bem - valor_entrada
        parcela_fin = calcula_parcela_price(valor_a_financiar, taxa_juros_anual_fin, prazo_meses_fin)
        custo_vp_fin = calcula_vp_custo_financiamento(valor_entrada, valor_a_financiar, taxa_juros_anual_fin, prazo_meses_fin, taxa_selic_anual)
        tabela_amortizacao = gera_tabela_amortizacao(valor_a_financiar, taxa_juros_anual_fin, prazo_meses_fin)

        # 2. Cálculos do Consórcio (cenário base: contemplação no final)
        parcela_con = calcula_parcela_consorcio(valor_bem, prazo_meses_con, taxa_adm_total, fundo_reserva_total)
        custo_vp_con = calcula_vp_custo_consorcio(parcela_con, prazo_meses_con, taxa_selic_anual)
        
        # 3. Exibição dos Resultados
        st.header("Resultados da Análise Comparativa")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Financiamento")
            st.metric(label="Custo Total em Valor Presente", value=f"R$ {custo_vp_fin:,.2f}")
            st.metric(label="Parcela Mensal", value=f"R$ {parcela_fin:,.2f}")
            total_pago_fin = valor_entrada + (parcela_fin * prazo_meses_fin)
            st.write(f"**Total Pago ao Final:** R$ {total_pago_fin:,.2f}")
            with st.expander("Ver Tabela de Amortização"):
                st.dataframe(tabela_amortizacao)

        with col2:
            st.subheader("Consórcio")
            st.metric(label="Custo Total em Valor Presente", value=f"R$ {abs(custo_vp_con):,.2f}")
            st.metric(label="Parcela Mensal Média", value=f"R$ {parcela_con:,.2f}")
            total_pago_con = parcela_con * prazo_meses_con
            st.write(f"**Total Pago ao Final:** R$ {total_pago_con:,.2f}")
            st.info("Cálculo do VP considera a contemplação no final do plano (pior cenário).")
            
        # --- Conclusão ---
        st.header("Conclusão")
        diferenca_vp = abs(custo_vp_fin - abs(custo_vp_con))
        if custo_vp_fin < abs(custo_vp_con):
            st.success(f"**O Financiamento parece ser mais vantajoso.** O seu custo em valor presente é R$ {diferenca_vp:,.2f} menor.")
        else:
            st.info(f"**O Consórcio parece ser mais vantajoso.** O seu custo em valor presente é R$ {diferenca_vp:,.2f} menor.")