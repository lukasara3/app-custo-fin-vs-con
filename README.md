# Comparador Financeiro: Financiamento vs. Consórcio

## 1. Resumo do Projeto

Esta é uma aplicação web interativa desenvolvida em Python e Streamlit que compara as modalidades de financiamento e consórcio para a aquisição de um bem. A ferramenta utiliza o conceito de **Valor do Dinheiro no Tempo** para determinar o custo efetivo de cada opção em valor presente, fornecendo uma recomendação clara e baseada em dados sobre qual modalidade é financeiramente mais vantajosa.

## 2. Funcionalidades Principais

- **Cálculo de Custo Efetivo:** Calcula o Valor Presente (VP) do custo total de um financiamento e de um consórcio.
- **Dados de Mercado em Tempo Real:** Utiliza a taxa Selic atual, obtida via API do Banco Central, como taxa de desconto para uma análise precisa do custo de oportunidade.
- **Análise de Sensibilidade:** Simula como a decisão pode mudar em cenários econômicos otimistas e pessimistas.
- **Relatório Visual:** Apresenta os resultados em tabelas e gráficos comparativos para facilitar a tomada de decisão.

## 3. Como Executar o Projeto

Siga os passos abaixo para rodar a aplicação em sua máquina local.

**Pré-requisitos:**
- Python 3.9 ou superior instalado.

**Passos:**

1.  **Clone o Repositório**
    ```bash
    git clone [URL_DO_SEU_REPOSITORIO]
    cd [NOME_DA_PASTA]
    ```

2.  **Crie e Ative um Ambiente Virtual**
    
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
    Ativar o venv: source .venv/bin/activate
    Desativar o venv: deactivate

3.  **Instale as Dependências**
    Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a Aplicação Streamlit**
    ```bash
    streamlit run app.py
    ```
    Após executar o comando acima, a aplicação será aberta automaticamente no seu navegador.

## 4. Como Rodar os Testes

Este projeto utiliza `pytest` para garantir a corretude dos cálculos financeiros. Para executar a suíte de testes, certifique-se de que o ambiente virtual está ativado e rode o seguinte comando na pasta raiz do projeto:

```bash
pytest
```
Você verá o resultado dos testes no terminal. Todos os testes devem passar para garantir que a lógica de cálculo está funcionando como esperado.

## 5. Estrutura do Projeto

- **/core:** Contém toda a lógica de negócio (cálculos financeiros, busca de dados, análises).
- **/tests:** Contém os testes unitários para garantir a corretude dos cálculos.
- **app.py:** Arquivo principal que define a interface do usuário e orquestra a aplicação.
- **pytest.ini:** Arquivo de configuração para o Pytest.
