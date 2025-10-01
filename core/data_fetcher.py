import requests
import streamlit as st

@st.cache_data(ttl=3600) # Atualiza a cada hora
def busca_taxa_selic_atual() -> float:
    """
    Busca a última taxa Selic meta anualizada na API do Banco Central do Brasil.
    Retorna a taxa em formato decimal (ex: 0.105 para 10.5%).
    Em caso de falha, retorna um valor padrão e exibe um aviso.
    """
    # Código da série no SGS para a Selic Meta: 432
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json"
    
    valor_padrao = 0.105 # 10.5% como fallback

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            dados = response.json()
            if dados:
                taxa_percentual = float(dados[0]['valor'])
                return taxa_percentual / 100
        else:
            # st.warning é um jeito elegante de mostrar avisos no Streamlit
            st.warning(f"Não foi possível buscar a Selic (Status: {response.status_code}). Usando taxa padrão de {valor_padrao*100}%.")
            return valor_padrao
            
    except requests.exceptions.RequestException:
        st.warning(f"Erro de conexão ao buscar a Selic. Usando taxa padrão de {valor_padrao*100}%.")
        return valor_padrao