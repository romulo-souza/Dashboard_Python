import streamlit as st
import pandas as pd
import plotly.express as px

# --- Configuração da Página ---
# Define o título da página, o ícone e o layout para ocupar a largura inteira
st.set_page_config(
    page_title="Dashboard de Salários Anuais na Área de Dados",
    page_icon="📊",
    layout="wide",
)

# --- Carregamento dos dados em cache para o csv ser baixado apenas uma vez e ser reutilizado para as mudanças de filtros (amenizar o delay) ---

@st.cache_data # retorno da função será armazenado em cache.
def carregar_dados():
    url = "https://raw.githubusercontent.com/romulo-souza/Dashboard_Python/refs/heads/main/data/df_tratado.csv"
    return pd.read_csv(url)

df = carregar_dados()

# --- Barra lateral (filtros) ---
st.sidebar.header("🔍 Filtros")

# Filtro de Ano
anos_disponiveis = sorted(df["ano"].unique())  # Seleciona valores únicos de ano e ordena do menor para o maior
anos_selecionados = st.sidebar.multiselect("Ano", anos_disponiveis, default=anos_disponiveis)

# Filtro de Senioridade
senioridades_disponiveis = sorted(df["senioridade"].unique())
senioridades_selecionadas = st.sidebar.multiselect("Senioridade", senioridades_disponiveis, default=senioridades_disponiveis)

# Filtro por Tipo de Contrato
contratos_disponiveis = sorted(df["contrato"].unique())
contratos_selecionados = st.sidebar.multiselect("Tipo de Contrato", contratos_disponiveis, default=contratos_disponiveis)

# Filtro por Tamanho da Empresa
tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())
tamanhos_selecionados = st.sidebar.multiselect("Tamanho da Empresa", tamanhos_disponiveis, default=tamanhos_disponiveis)

# --- Filtragem do DataFrame (aplicação do filtro) ---
# O DataFrame principal é filtrado com base nas seleções feitas na barra lateral. Seleciona apenas as linhas que atendem a TODAS as condições listadas.

#Esse código mantém no df_filtrado apenas as linhas que:
#O ano está em anos_selecionados
#A senioridade está em senioridades_selecionadas
#O contrato está em contratos_selecionados
#O tamanho da empresa está em tamanhos_disponiveis
#ou seja, o isin() verifica se cada valor da coluna está contido na lista passada, retornando true ou false para cada linha'''
df_filtrado = df[
    (df["ano"].isin(anos_selecionados)) & 
    (df["senioridade"].isin(senioridades_selecionadas)) &
    (df["contrato"].isin(contratos_selecionados)) &
    (df['tamanho_empresa'].isin(tamanhos_selecionados))
]

# --- Conteúdo Principal ---
st.title("🎲 Dashboard de Análise de Salários na Área de Dados")
st.markdown("Explore os dados salariais na área de dados nos últimos anos. Utilize os filtros à esquerda para refinar sua análise.")

# Métricas Principais (KPIs) (pode pegar ideias do .describe ou .info que usamos para entender a base)
st.subheader("Métricas gerais (Salário anual em USD)")

#caso df_filtrado não esteja vazio
if not df_filtrado.empty:
    salario_medio = df_filtrado["salario_usd"].mean()
    salario_maximo = df_filtrado["salario_usd"].max()
    total_registros = df_filtrado.shape[0] # [0] para pegar somente a qtd de linhas do df
    cargo_mais_frequente = df_filtrado["cargo"].mode()[0] #[0] pega a primeira moda caso haja mais de uma
else:
    salario_medio, salario_maximo, total_registros, cargo_mais_frequente = 0, 0, 0, ""

# Divide as informações em 4 colunas dentro da página
col1, col2, col3, col4 = st.columns(4)
col1.metric("Salário médio", f"${salario_medio:,.0f}") #:,.0f → formatação numérica: ',' separador de milhar e '.0f' valor float sem casas decimais (arredondado)
col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
col3.metric("Total de registros", f"{total_registros:,}")
col4.metric("Cargo mais frequente", cargo_mais_frequente)

st.divider() #divisor

# --- Análises Visuais com Plotly ---
st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1: # with entra no “contexto” dessa coluna e tudo o que criar dentro do bloco já será renderizada nela
    if not df_filtrado.empty:
        #maiores salários médios anuais por cargo (top 10)
        top_cargos = df_filtrado.groupby('cargo')['salario_usd'].mean().nlargest(10).sort_values(ascending=True).reset_index()
        grafico_cargos = px.bar(
            top_cargos,
            x='salario_usd',
            y='cargo',
            orientation='h',
            title='Top 10 Cargos por Salário Médio Anual',
            labels={'salario_usd': 'Salário Médio Anual (USD)', 'cargo': 'Cargo'},
            color_discrete_sequence=['#00BFFF']  
        )
        grafico_cargos.update_layout(title_x = 0.1, yaxis = {'categoryorder': 'total ascending'})
        grafico_cargos.update_traces(hovertemplate='%{y}: $%{x:,.0f}') #texto quando passar o mouse sobre o gráfico
        st.plotly_chart(grafico_cargos, use_container_width=True)
    else:
        st.warning("Sem dados para exibir no gráfico Top 10 Cargos por Salário Médio Anual.")
    
with col_graf2:
    if not df_filtrado.empty:
        # gráfico de histograma da distribuição salarial anual
        grafico_hist = px.histogram(
            df_filtrado,
            x='salario_usd',
            nbins=35,
            title='Distribuição de Salários Anuais',
            labels={'salario_usd':'Faixa salarial (USD)'},
            color_discrete_sequence=['#00BFFF'],
        )
        grafico_hist.update_yaxes(title_text="Quantidade")
        grafico_hist.update_layout(title_x=0.1)
        grafico_hist.update_traces(hovertemplate='Faixa salarial (USD): %{x}<br>Quantidade: %{y:,.0f}')
        st.plotly_chart(grafico_hist, use_container_width=True)
    else:
        st.warning("Sem dados para exibir no gráfico de Distribuição Salários Anuais.")
    
col_graf3, col_gaf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        # Gráfico de rosca da porcentagem do regime de trabalho
        regime_trabalho_contagem = df_filtrado['regime_trabalho'].value_counts().reset_index()
        regime_trabalho_contagem.columns = ['regime_trabalho', 'quantidade'] #renomeando a segunda coluna de 'count' para 'quantidade'
        grafico_regime_trabalho = px.pie(
            regime_trabalho_contagem,
            names='regime_trabalho',
            values='quantidade',
            title = 'Proporção dos Regimes de Trabalho',
            hole=0.5,
            color_discrete_sequence = ["#2F2E94", "#325194", "#4C64FE"]
        )
        grafico_regime_trabalho.update_traces(textinfo='percent+label', hovertemplate='Regime: %{label}<br>Quantidade: %{value:,.0f}')
        grafico_regime_trabalho.update_layout(
            margin=dict(l = 48),  # aumenta margem esquerda (l) para a barra de filtro não cortar o label 'hibrido'
            title_x=0.1
        )
        st.plotly_chart(grafico_regime_trabalho, use_container_width=True)
    else:
        st.warning("Sem dados para exibir no gráfico de Proporção dos Regimes de Trabalho.")


with col_gaf4:
    if not df_filtrado.empty:
        # Agrupar media salarial anual de cientista de dados por país 
        media_salario_pais_CD = (
            df_filtrado[df_filtrado['cargo'] == 'Data Scientist'] # Faz o filtro de cargo primeiro
            .groupby(['residencia_iso3'])['salario_usd'] # Depois o agrupamento
            .mean()
            .sort_values(ascending=False)
            .reset_index()
        )
        grafico_paises = px.choropleth(
            media_salario_pais_CD,
            locations = 'residencia_iso3',
            color = 'salario_usd', # a cor de cada país vai depender do valor do salário médio.
            color_continuous_scale = 'rdylgn', # a escala de cores usada será vermelho -> amarelo -> verde, indicando valores baixos a altos.
            title = 'Salário médio anual de Cientista de Dados por País',
            labels={'salario_usd': 'Salário médio anual (USD)', 'residencia_iso3': 'País'},
            hover_name = 'residencia_iso3'
        )
        grafico_paises.update_layout(title_x=0.1)
        grafico_paises.update_traces(hovertemplate='País: %{location}<br>Salário médio anual (USD): %{z:,.2f}')
        st.plotly_chart(grafico_paises, use_container_width=True)
    else:
        st.warning("Sem dados para exibir no gráfico de países.")

# --- Tabela com os Dados Detalhados ---
st.subheader("Dados detalhados de acordo com os filtros aplicados")
st.dataframe(df_filtrado)
st.download_button(
    label="⬇️ Baixar dados detalhados (CSV)",
    data=df_filtrado.to_csv(index=False),
    file_name="dados_filtrados.csv",
    mime="text/csv"
)
