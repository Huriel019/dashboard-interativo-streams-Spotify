import pandas as pd
import streamlit as st
import plotly.express as px

df = pd.read_csv("Spotify_tratado.csv")

st.set_page_config(
    page_title="Dashboard de streams Spotify", 
    page_icon="📊",
    layout="wide",
)

st.sidebar.header("🔍 Filtros")

paises_disponiveis = sorted(df["País"].unique())
paises_selecionados = st.sidebar.multiselect("País", paises_disponiveis, default=paises_disponiveis)

generos_disponiveis = sorted(df["Gênero"].unique())
generos_selecionados = st.sidebar.multiselect("Gênero", generos_disponiveis, default=generos_disponiveis)

artistas_disponiveis = sorted(df["Artista"].unique())
artistas_selecionados = st.sidebar.multiselect("Artistas", artistas_disponiveis, default=artistas_disponiveis)

genero_musical = sorted(df["Gênero principal"].unique())
genero_musical_selecionado = st.sidebar.multiselect("Gênero musical", genero_musical, default=genero_musical)

tipos_disponiveis = sorted(df["Tipo de artista"].unique())
tipos_selecionados = st.sidebar.multiselect("Tipo de artista", tipos_disponiveis, default=tipos_disponiveis)

df_filtrado = df[
    (df["País"].isin(paises_selecionados))&
    (df["Gênero"].isin(generos_selecionados))&
    (df["Artista"].isin(artistas_selecionados))&
    (df["Gênero principal"].isin(genero_musical_selecionado))&
    (df["Tipo de artista"].isin(tipos_selecionados))
]

st.title("Dashboard interativo de streams do Spotify")
st.markdown("Explore diversas funções, utilize a barra lateral a esquerda para refinar sua pesquisa")

st.subheader("Métricas Gerais")

if not df_filtrado.empty:
    artista_mais_ouvido = df_filtrado["Artista"].value_counts().idxmax()
    genero_musical_mais_ouvido = df_filtrado["Gênero principal"].value_counts().idxmax()
    pais_mais_artistas = df_filtrado["País"].value_counts().idxmax()
    genero_mais_ouvido = df_filtrado["Gênero"].value_counts().idxmax()
    
else:
    artista_mais_ouvido, genero_musical_mais_ouvido, pais_mais_artistas, genero_mais_ouvido = 0, 0, 0, ""
    
col1, col2, col3, col4 = st.columns(4)
col1.metric("Artista mais ouvido",artista_mais_ouvido)    
col2.metric("Gênero musical mais escutado", genero_musical_mais_ouvido)
col3.metric("País com mais asrtistas", pais_mais_artistas)
col4.metric("Gênero mais escutado", genero_mais_ouvido)

st.markdown("---")

st.subheader("Gráficos")

col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    if not df_filtrado.empty:
        top_artistas = df_filtrado.groupby("Artista")["Streams totais (Milhões)"].sum().sort_values(ascending=False).head(10).reset_index()
        grafico_artistas = px.bar(
            top_artistas, 
            x="Streams totais (Milhões)",
            y="Artista",
            orientation="h",
            title="Artistas com mais Streams (Milhões)",
            labels={'Streams totais (Milhões)': "", 'Artista': ""}
        )
        grafico_artistas.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'}, hovermode='closest')
        grafico_artistas.update_traces(
    texttemplate="%{x:,.0f}",
    textposition="auto",
    hovertemplate="<b>%{y}</b><br>" +
                  "Total de Streams: %{x:,.0f}<extra></extra>")
        st.plotly_chart(grafico_artistas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de artistas")    
        

with col_graf2:
    if not df_filtrado.empty:
        top_generos_tocados = df_filtrado["Gênero principal"].value_counts().sort_values().reset_index()
        grafico_generos_tocados = px.bar(
            top_generos_tocados,
            x="count",
            y="Gênero principal",
            title="Gêneros mais escutados",
            labels={"count":"Contagem", "Gênero principal": "Gênero musical"}
        )
        grafico_generos_tocados.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})  
        st.plotly_chart(grafico_generos_tocados, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de gêneros musicais")     
        
col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        top_idioma =  df_filtrado["Idioma"].value_counts().sort_values(ascending=False).reset_index()
        grafico_idiomas = px.bar(
            top_idioma,
            x="Idioma",
            y="count",
            title="Top idiomas dos artistas",
            labels={"Idioma":"", "count":"contagem"}
        )
        grafico_idiomas.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'}) 
        st.plotly_chart(grafico_idiomas, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico de idiomas")                     
        
with col_graf4:
    if not df_filtrado.empty:
        tipo_artista = df_filtrado["Tipo de artista"].value_counts().reset_index()
        tipo_artista.columns = ["tipo_artista", "Quantidade"]
        grafico_tipo = px.pie(
            tipo_artista,
            names="tipo_artista",
            values="Quantidade",
            title="Tipo de artista mais comum"
        )
        grafico_tipo.update_traces(textinfo='percent+label')
        grafico_tipo.update_layout(title_x=0.1)
        st.plotly_chart(grafico_tipo, width="stretch")
        
    else:
        st.warning("Nenhum dado para exibir no gráfico de tipo de artista")
        

streams_pais = df_filtrado.groupby("País")["Streams totais (Milhões)"].sum().head(10).sort_values(ascending=False).reset_index()
grafico_streams = px.bar(
    streams_pais,
    x="País",
    y="Streams totais (Milhões)",
    title="Top 10 paises com mais streams",
    labels={"País":'Paises', "Streams totais (Milhões)":'' }
)
grafico_streams.update_layout(title_x=0.1, yaxis={'categoryorder':'total ascending'})
st.plotly_chart(grafico_streams, use_container_width=True)