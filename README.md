# Dashboard de Análise de Salários na Área de Dados

Link do dashboard:

Projeto desenvolvido durante a **Imersão Dados com Python** promovida pela Alura.

Trata-se da criação de um **dashboard interativo em Python**, desde o **tratamento dos dados** no Google Colab até o **deploy do dashboard** utilizando Streamlit.

## O dashboard permite explorar dados salariais de profissionais da área de dados, com aplicação de filtros e exibição de gráficos interativos.

## Funcionalidades

- Filtros interativos:
  - Ano
  - Senioridade
  - Tipo de Contrato
  - Tamanho da Empresa

- Métricas Gerais:
  - Salário médio
  - Salário máximo
  - Total de registros
  - Cargo mais frequente
  
- Gráficos interativos com Plotly:
  - Top 10 cargos por salário médio anual
  - Distribuição de salários anuais (histograma)
  - Proporção de regimes de trabalho (gráfico de rosca)
  - Salário médio anual de Cientista de Dados por país (mapa)

- Visualização de dados detalhados em tabela

- Download dos dados detalhados

---

## Tecnologias utilizadas

- Python 3
- Pandas
- Plotly
- Streamlit
- Google Colab (para análise exploratória, tratamento e visualização dos dados)

## Como executar o projeto localmente

1. **Clonar o repositório**

2. **Criar o ambiente virtual**
   `shell python -m venv .venv`

3. **Ativar o ambiente virtual**
   Windows: `shell .venv\Scripts\Activate`

Linux/Mac: `shell source .venv/bin/activate`

4. **Instalar as dependências**
   `shell pip install -r requirements.txt`

5. **Executar o código**
   `shell streamlit run app.py`
