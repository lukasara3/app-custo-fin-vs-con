import plotly.graph_objects as go
import pandas as pd

def plot_custo_total_bar_chart(vp_fin: float, vp_con: float) -> go.Figure:
    """
    Cria um gráfico de barras comparando o Custo em Valor Presente do Financiamento vs. Consórcio.
    """
    fig = go.Figure(data=[
        go.Bar(name='Financiamento', x=['Custo Total em VP'], y=[vp_fin], text=f"R$ {vp_fin:,.2f}", textposition='auto'),
        go.Bar(name='Consórcio', x=['Custo Total em VP'], y=[vp_con], text=f"R$ {vp_con:,.2f}", textposition='auto')
    ])
    fig.update_layout(
        title_text='Comparativo de Custo Total em Valor Presente (VP)',
        yaxis_title="Custo em VP (R$)",
        barmode='group'
    )
    return fig

def plot_scenario_analysis_bar_chart(df_cenarios: pd.DataFrame) -> go.Figure:
    """
    Cria um gráfico de barras agrupado para a análise de cenários.
    """
    # Precisamos converter as colunas de custo de string para float para o gráfico
    df_plot = df_cenarios.copy()
    df_plot['VP Custo Financiamento (R$)'] = df_plot['VP Custo Financiamento (R$)'].str.replace('R$ ', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
    df_plot['VP Custo Consórcio (R$)'] = df_plot['VP Custo Consórcio (R$)'].str.replace('R$ ', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)

    fig = go.Figure(data=[
        go.Bar(name='Financiamento', x=df_plot.index, y=df_plot['VP Custo Financiamento (R$)'], text=df_plot['VP Custo Financiamento (R$)'].apply(lambda x: f'R$ {x:,.2f}'), textposition='auto'),
        go.Bar(name='Consórcio', x=df_plot.index, y=df_plot['VP Custo Consórcio (R$)'], text=df_plot['VP Custo Consórcio (R$)'].apply(lambda x: f'R$ {x:,.2f}'), textposition='auto')
    ])
    fig.update_layout(
        title_text='Comparativo de Custos nos Diferentes Cenários',
        xaxis_title="Cenário",
        yaxis_title="Custo em VP (R$)",
        barmode='group'
    )
    return fig