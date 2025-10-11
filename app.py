import streamlit as st
import pandas as pd
from core.calculations import *
from core.data_fetcher import busca_taxa_selic_atual
from core.analysis import *
from core.plotting import plot_custo_total_bar_chart, plot_scenario_analysis_bar_chart

# --- Configuração da Página ---
st.set_page_config(page_title="Calculadora Estratégica", page_icon="💰", layout="wide")

st.title("Calculadora Estratégica: Financiamento vs. Consórcio")
st.markdown("Uma ferramenta para análise do custo efetivo de aquisição de bens, baseada no Valor do Dinheiro no Tempo.")

# Inicializa o session_state para guardar a "memória" da aplicação
if 'analysis_run' not in st.session_state:
    st.session_state.analysis_run = False
    st.session_state.params = {}

# --- Barra Lateral para Inputs do Usuário ---
st.sidebar.header("Parâmetros de Entrada")

# PARÂMETRO GLOBAL - Taxa de Oportunidade (Selic)
selic_atual = busca_taxa_selic_atual()
taxa_selic_anual = st.sidebar.slider(
    "Taxa de Oportunidade (Selic Anual %)", 
    min_value=1.0, max_value=20.0, value=selic_atual * 100, step=0.25
) / 100
st.sidebar.caption(f"Taxa Selic Meta atual detectada: {selic_atual*100:.2f}% a.a.")

# EXPANDER 1 - Dados do Financiamento
with st.sidebar.expander("Dados do Financiamento", expanded=True):
    valor_bem = st.number_input("Valor do Bem (R$)", min_value=1000, value=300000, step=5000)
    valor_entrada = st.number_input("Valor da Entrada (R$)", min_value=0, value=60000, step=1000)
    taxa_juros_anual_fin = st.slider("Taxa de Juros do Financiamento Anual (%)", min_value=1.0, max_value=25.0, value=11.5, step=0.25) / 100
    prazo_meses_fin = st.slider("Prazo do Financiamento (meses)", min_value=12, max_value=420, value=360, step=12)

# EXPANDER 2 - Dados do Consórcio
with st.sidebar.expander("Dados do Consórcio", expanded=True):
    prazo_meses_con = st.slider("Prazo do Grupo do Consórcio (meses)", min_value=12, max_value=240, value=180, step=12)
    taxa_adm_total = st.slider("Taxa de Administração Total (%)", min_value=5.0, max_value=30.0, value=18.0, step=0.5)
    fundo_reserva_total = st.slider("Fundo de Reserva Total (%)", min_value=0.0, max_value=5.0, value=1.0, step=0.25)

# --- Botão para Executar os Cálculos ---
if st.sidebar.button("Analisar", type="primary", use_container_width=True):
    if valor_entrada >= valor_bem:
        st.error("O valor da entrada não pode ser maior ou igual ao valor do bem.")
        st.session_state.analysis_run = False
    else:
        st.session_state.analysis_run = True
        st.session_state.params = {
            'valor_bem': valor_bem, 'valor_entrada': valor_entrada,
            'taxa_juros_anual_fin': taxa_juros_anual_fin, 'prazo_meses_fin': prazo_meses_fin,
            'taxa_selic_anual': taxa_selic_anual, 'prazo_meses_con': prazo_meses_con,
            'taxa_adm_total': taxa_adm_total, 'fundo_reserva_total': fundo_reserva_total
        }

# --- Lógica de Exibição (só roda se a análise foi iniciada) ---
if st.session_state.analysis_run:
    params = st.session_state.params
    valor_a_financiar = params['valor_bem'] - params['valor_entrada']
    parcela_fin = calcula_parcela_price(valor_a_financiar, params['taxa_juros_anual_fin'], params['prazo_meses_fin'])
    parcela_con = calcula_parcela_consorcio(params['valor_bem'], params['prazo_meses_con'], params['taxa_adm_total'], params['fundo_reserva_total'])
    params.update({
        'valor_a_financiar': valor_a_financiar, 'parcela_fin': parcela_fin,
        'parcela_con': parcela_con, 'carta_credito': params['valor_bem']
    })

    tab1, tab2, tab3 = st.tabs(["📊 Resultado Principal", "📈 Análise de Cenários", "🎯 Estratégias de Consórcio"])

    with tab1:
        custo_vp_fin = calcula_vp_custo_financiamento(params['valor_entrada'], params['valor_a_financiar'], params['taxa_juros_anual_fin'], params['prazo_meses_fin'], params['taxa_selic_anual'])
        custo_vp_con = calcula_vp_custo_consorcio(params['parcela_con'], params['prazo_meses_con'], params['taxa_selic_anual'])
        
        st.header("Resultados da Análise (Cenário Realista)")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Financiamento")
            st.metric(label="Custo Total em Valor Presente", value=f"R$ {custo_vp_fin:,.2f}")
            st.metric(label="Parcela Mensal", value=f"R$ {parcela_fin:,.2f}")
            with st.expander("Ver Tabela de Amortização"):
                tabela_amortizacao = gera_tabela_amortizacao(valor_a_financiar, params['taxa_juros_anual_fin'], params['prazo_meses_fin'])
                st.dataframe(tabela_amortizacao)
        with col2:
            st.subheader("Consórcio")
            st.metric(label="Custo Total em Valor Presente", value=f"R$ {abs(custo_vp_con):,.2f}")
            st.metric(label="Parcela Mensal Média", value=f"R$ {parcela_con:,.2f}")
            st.info("Cálculo do VP considera a contemplação no final do plano (pior cenário).")
        
        st.subheader("Gráfico Comparativo de Custos")
        fig_comparativo = plot_custo_total_bar_chart(custo_vp_fin, abs(custo_vp_con))
        st.plotly_chart(fig_comparativo, use_container_width=True)

        diferenca_vp = abs(custo_vp_fin - abs(custo_vp_con))
        if custo_vp_fin < abs(custo_vp_con):
            st.success(f"**Conclusão:** No cenário realista, o **Financiamento** parece ser mais vantajoso por uma diferença de R$ {diferenca_vp:,.2f} em valor presente.")
        else:
            st.info(f"**Conclusão:** No cenário realista, o **Consórcio** parece ser mais vantajoso por uma diferença de R$ {diferenca_vp:,.2f} em valor presente.")

    with tab2:
        st.header("Análise de Sensibilidade à Taxa de Oportunidade (Selic)")
        st.markdown("Esta análise mostra como a decisão pode mudar se a taxa de juros da economia (Selic) variar.")
        df_cenarios = run_scenario_analysis(params)
        st.table(df_cenarios)
        st.subheader("Gráfico Comparativo dos Cenários")
        fig_cenarios = plot_scenario_analysis_bar_chart(df_cenarios)
        st.plotly_chart(fig_cenarios, use_container_width=True)

    with tab3:
        st.header("Simulador de Estratégias para o Consórcio")
        st.info("Explore cenários alternativos para sua carta de consórcio, tratando-a como um ativo financeiro.")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Estratégia de Lance")
            lance_perc = st.slider("Lance Ofertado (% da carta)", 0, 100, 25, key="lance_perc")
            if st.button("Simular Lance"):
                resultado = simular_estrategia_lance(params['parcela_con'], params['prazo_meses_con'], params['carta_credito'], lance_perc, params['taxa_selic_anual'])
                st.metric("Novo Custo em VP (com lance)", f"R$ {resultado['custo_vp']:,.2f}")
                st.write(f"Prazo efetivo reduzido para ~{resultado['novo_prazo']} meses.")
        with col2:
            st.subheader("Estratégia de Venda")
            mes_contemplacao_venda = st.slider("Mês da Contemplação (p/ Venda)", 1, params['prazo_meses_con'], int(params['prazo_meses_con']/2), key="mes_venda")
            agio_venda = st.slider("Ágio na Venda (% sobre valor pago)", -10, 50, 15, key="agio_venda")
            if st.button("Simular Venda da Cota"):
                resultado = simular_estrategia_venda(params['parcela_con'], mes_contemplacao_venda, agio_venda, params['taxa_selic_anual'])
                st.metric("VPL da Operação", f"R$ {resultado['vpl']:,.2f}")
                st.metric("TIR Anualizada", f"{resultado['tir_anual']:.2%}")
        with col3:
            st.subheader("Estratégia de Aluguel")
            mes_contemplacao_aluguel = st.slider("Mês da Contemplação (p/ Aluguel)", 1, params['prazo_meses_con'], int(params['prazo_meses_con']/4), key="mes_aluguel")
            valor_aluguel = st.number_input("Valor Mensal do Aluguel (R$)", value=int(params['carta_credito']*0.005), key="valor_aluguel")
            if st.button("Simular Aluguel do Bem"):
                resultado = simular_estrategia_aluguel(params['parcela_con'], params['prazo_meses_con'], mes_contemplacao_aluguel, valor_aluguel, params['taxa_selic_anual'])
                st.metric("VPL da Operação", f"R$ {resultado['vpl']:,.2f}")
                if resultado['vpl'] > 0:
                    st.success("VPL positivo: as receitas de aluguel superam os custos das parcelas em valor presente.")
                else:
                    st.warning("VPL negativo: os custos superam as receitas em valor presente.")