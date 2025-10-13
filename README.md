# Comparador Financeiro: Financiamento vs. Consórcio
Allan Dayrell - 2022035563
Lucas Araujo - 2022035962

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

---

# Utilizando a ferramenta

Ao abrir a aplicação, você verá a tela dividida em dois lados:

- **À esquerda**: Um painel cinza com campos para entrada de dados
- **À direita**: Um grande espaço em branco (ficará preenchido após clicar em "Analisar")

## Preenchendo os dados

### Taxa de Oportunidade (Selic)

**O que é?** É a taxa de juros da economia. Representa quanto você ganharia se colocasse o dinheiro na poupança/tesouro direto.

**O que fazer:**

- Veja o campo no topo: "Taxa de Oportunidade (Selic Anual %)"
- Ele já virá com um valor automático detectado (ex: 15.00%)
- Você pode deslizar a bolinha para mudar o valor ou deixar como está

**Por que importa?** Quanto maior a Selic, mais cara fica a opção que estica seus pagamentos no tempo (consórcio).

### **Informe o Valor do Bem**

**O que é?** O preço total daquilo que você quer comprar.

**O que fazer:**

- Abaixo da Selic, clique no campo "Valor do Bem (R$)"
- Digite o valor. Exemplo: 300000 (para R$ 300 mil)
- Pressione Enter ou clique fora do campo

**Dica:** Este valor afeta AMBAS as opções (financiamento e consórcio).

### **Dados do FINANCIAMENTO**

**Valor da Entrada (R$)**

- Quanto você vai pagar de forma imediata
- O restante será financiado
- Exemplo: Se o bem custa R$ 300 mil e você entra com R$ 60 mil, financiará R$ 240 mil

**Taxa de Juros do Financiamento Anual (%)**

- O juros que o banco cobra por mês (convertido para taxa anual)
- Varia muito conforme o banco, tipo de bem, seu score de crédito
- Típico: 6% a 20% ao ano

**Prazo do Financiamento (meses)**

- Quantos meses para terminar de pagar
- Comum: 12 a 360 meses (até 30 anos)
- Quanto menor o prazo, maiores as parcelas (mas menos juros pagos no total)

### **Dados do CONSÓRCIO**

**Prazo do Grupo do Consórcio (meses)**

- Quanto tempo o consórcio vai funcionar
- Tipicamente: 12 a 180 meses
- Você pode ser sorteado antes e parar de pagar

**Taxa de Administração Total (%)**

- Quanto a administradora do consórcio cobra (em % do valor do bem)
- Típico: 15% a 25%

**Fundo de Reserva Total (%)**

- Um fundo de segurança (em % do valor)
- Você pode sacar no final se ninguém deixar de pagar
- Típico: 1% a 5%

### **Analisar**

Depois que tiver preenchido todos os campos, clique no botão **"Analisar"** no final do painel.

# Resultados

Após clicar em "Analisar", o lado direito da tela vai mostrar informações em **3 abas**:

## **ABA 1: 📊 Resultado Principal**

### **Coluna FINANCIAMENTO:**

- **Custo Total em Valor Presente**: O custo REAL (em dinheiro de hoje) considerando entrada + todas as parcelas
- **Parcela Mensal**: Quanto você paga todo mês

### **Coluna CONSÓRCIO:**

- **Custo Total em Valor Presente**: O custo REAL do consórcio (considerando que você é sorteado no último mês)
- **Parcela Mensal Média**: Quanto você pagaria por mês em média

### **Gráfico Comparativo:**

Compara visualmente qual é mais barato.

### **Conclusão:**

A ferramenta dirá qual opção é mais vantajosa e por quanto.

**IMPORTANTE:** O maior número não é necessariamente o "pior". O que importa é o **Custo em Valor Presente** — aquele que tiver o número MENOR é o mais barato.

---

## **ABA 2: 📈 Análise de Cenários**

Mostra o que aconteceria se a Selic mudasse:

- Tabela com diferentes cenários (Selic a 8%, 10%, 15%, 20%, etc.)
- Para cada cenário, mostra qual opção é mais barata
- Útil para entender: "E se os juros da economia subissem/caíssem?"

---

## **ABA 3: 🎯 Estratégias de Consórcio**

Para quem quer explorar o consórcio de formas mais criativas:

- **Estratégia de Lance**: Ofertar um lance para comprar a cota antes do sorteio
- **Estratégia de Venda**: Vender a cota sorteada com ágio
- **Estratégia de Aluguel**: Comprar pelo consórcio e alugar o bem

Não é obrigatório usar — é só para explorar cenários mais avançados.

