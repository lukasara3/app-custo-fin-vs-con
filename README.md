# Comparador Financeiro: Financiamento vs. Consórcio

## 1. Resumo do Projeto

Esta é uma aplicação web interativa desenvolvida em Python e Streamlit que compara as modalidades de financiamento e consórcio para a aquisição de um bem. A ferramenta utiliza o conceito de **Valor do Dinheiro no Tempo** para determinar o custo efetivo de cada opção em valor presente, fornecendo uma recomendação clara e baseada em dados sobre qual modalidade é financeiramente mais vantajosa.

## 2. Funcionalidades Principais

- **Análise de Custo Efetivo:** Calcula e compara o Valor Presente (VP) do custo total de um financiamento e de um consórcio.
- **Dados de Mercado:** Utiliza a taxa Selic atual, obtida em tempo real através da API do Banco Central do Brasil, como a taxa de desconto para os cálculos. Isso reflete o custo de oportunidade do dinheiro de forma precisa.
- **Análise de Cenários:** Simula o impacto de cenários econômicos otimistas e pessimistas na decisão final.
- **Relatórios Visuais:** Apresenta os resultados em tabelas e gráficos fáceis de entender, facilitando a interpretação dos dados.

## 3. Estrutura do Projeto

- **/core:** Possui toda a lógica de negócio. Ela contém todos os módulos com a lógica de negócio, como as funções para os cálculos financeiros, a busca da taxa Selic na API do Banco Central e a análise de cenários.
- **app.py:** Este é o arquivo principal que executa a aplicação. Ele é responsável por criar toda a interface que o usuário vê no navegador (títulos, campos de entrada, botões e gráficos) e por chamar as funções de cálculo.
- - **/tests:** Contém os testes unitários feitos para garantir a corretude dos cálculos.
- **pytest.ini:** Arquivo de configuração para o Pytest.

## 4. Guia de Instalação e Execução

Este guia prático mostra como baixar o projeto e executar a aplicação em seu computador.

### Pré-requisitos

Python 3.9 ou superior instalado. Você pode baixá-lo em python.org.

**Passos:**

1.  **Clone o Repositório:**
   Abra um terminal (Prompt de Comando ou PowerShell no Windows, Terminal no macOS/Linux) e execute o comando abaixo:
    ```bash
    git clone https://github.com/lukasara3/app-custo-fin-vs-con.git
    ```
    Depois, navegue para a pasta do projeto:
     ```bash
    cd app-custo-fin-vs-con
    ```

2.  **Crie e Ative um Ambiente Virtual:**
    
    *No Windows:*
    ```bash
    python -m venv .venv
    .\.venv\Scripts\activate
    ```
    
    *No macOS / Linux:*
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
    Se o comando funcionar, você verá (.venv) no início da linha do seu terminal.
    Ativar o venv: source .venv/bin/activate
    Desativar o venv: deactivate

4.  **Instale as Dependências:**
    Com o ambiente virtual ativado, instale as bibliotecas que o projeto precisa para funcionar. O arquivo requirements.txt lista todas elas. Execute o comando:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a Aplicação Streamlit:**
    ```bash
    streamlit run app.py
    ```
    
    O terminal exibirá uma mensagem indicando que a aplicação está rodando e fornecerá as URLs para acessá-la, como no exemplo abaixo:
    ```bash
    You can now view your Streamlit app in your browser.
    
      Local URL: http://localhost:8501
      Network URL: http://172.27.113.180:8501```
    ```
    
6. **Acessar no Navegador:**
    Copie a **`Local URL`** que apareceu no seu terminal. O endereço padrão é `http://localhost:8501`.
    Abra seu navegador de internet (Google Chrome, Firefox, etc.) e cole a URL na barra de endereços. Ou segure CTRL + Clque no link `http://localhost:8501`.

    Pronto! A interface do comparador financeiro será carregada no seu navegador. Agora você pode interagir com a ferramenta, inserir os dados e analisar os resultados.

## 5. Como Rodar os Testes (opcional)

Este projeto utiliza `pytest` para garantir a corretude dos cálculos financeiros. Para executar a suíte de testes, certifique-se de que o ambiente virtual está ativado e rode o seguinte comando na pasta raiz do projeto:

```bash
pytest
```
Você verá o resultado dos testes no terminal. Todos os testes devem passar para garantir que a lógica de cálculo está funcionando como esperado.
