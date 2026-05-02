import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(page_title="Análise de Comportamento do Consumidor", layout="wide")

# 2. Definição do Padrão de Cores (Seu Guia de Estilo)
COR_FUNDO = "#0B1120"
COR_TEXTO = "#D1D5DB"
COR_GRID = "#374151"
COR_AZUL_PRINCIPAL = "#3B82F6"
COR_PONTOS_LINHA = "#93C5FD"

# Paleta específica para métodos de pagamento (Mapeamento Direto)
# Nota: Verifique se os nomes abaixo batem com os nomes no seu arquivo CSV
PALETA_PAGAMENTOS = {
    "Credit Card": "#3B82F6",      
    "Venmo": "#8B5CF6",            
    "Cash": "#10B981",             
    "PayPal": "#F59E0B",           
    "Debit Card": "#6366F1",       
    "Bank Transfer": "#EC4899"     
}

# 3. Estilo CSS para o Fundo Escuro
st.markdown(f"""
    <style>
    .main {{ background-color: {COR_FUNDO}; }}
    [data-testid="stMetricValue"] {{ color: {COR_AZUL_PRINCIPAL}; }}
    h1, h2, h3, p, span, label {{ color: {COR_TEXTO} !important; }}
    </style>
    """, unsafe_allow_html=True)

# 4. Carregar Dados
df = pd.read_csv("shopping_trends.csv")

# 5. Título
st.title("📊 dashboard | análise do comportamento do consumidor")
st.markdown("---")

# 6. Sidebar - Filtros
st.sidebar.header("Filtros de Pesquisa")
genero = st.sidebar.multiselect("Gênero:", options=df['Gender'].unique(), default=df['Gender'].unique())
categoria = st.sidebar.multiselect("Categoria:", options=df['Category'].unique(), default=df['Category'].unique())

# Filtro Dinâmico
df_selection = df.query("Gender == @genero & Category == @categoria")

# 7. KPI - Faturamento
total_faturamento = df_selection['Purchase Amount (USD)'].sum()
faturamento_texto = f"R$ {total_faturamento/1_000_000:.2f} Mi" if total_faturamento >= 1_000_000 else f"R$ {total_faturamento/1_000:.1f} Mil"

st.metric("Faturamento Total Selecionado", faturamento_texto)

# 8. Layout de Gráficos
col1, col2 = st.columns(2)

with col1:
    # --- Gráfico 1: Evolução (Barras + Tendência) ---
    df_evol = df_selection.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
    fig_evol = px.bar(df_evol, x='Season', y='Purchase Amount (USD)',
                      title="Evolução de Faturamento por Temporada",
                      color_discrete_sequence=[COR_AZUL_PRINCIPAL], template="plotly_dark")
    
    # Linha de tendência branca com pontos em azul claro
    fig_evol.add_scatter(x=df_evol['Season'], y=df_evol['Purchase Amount (USD)'],
                         mode='lines+markers', line=dict(color='#FFFFFF', width=2), 
                         marker=dict(color=COR_PONTOS_LINHA, size=8), name='Tendência')
    
    fig_evol.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          yaxis=dict(gridcolor=COR_GRID), xaxis=dict(gridcolor=COR_GRID), showlegend=False)
    st.plotly_chart(fig_evol, use_container_width=True)

    # --- Gráfico 2: Ranking de Pagamentos (CORES ESPECÍFICAS) ---
    df_pag = df_selection.groupby('Payment Method').size().reset_index(name='Qtd').sort_values('Qtd', ascending=True)
    
    fig_pag = px.bar(df_pag, x='Qtd', y='Payment Method', orientation='h',
                     title="Ranking: Métodos de Pagamento",
                     color='Payment Method', 
                     color_discrete_map=PALETA_PAGAMENTOS, 
                     template="plotly_dark")
    
    fig_pag.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', showlegend=False)
    st.plotly_chart(fig_pag, use_container_width=True)

with col2:
    # --- Gráfico 3: Ranking de Categorias ---
    df_cat = df_selection.groupby('Category').size().reset_index(name='vendas').sort_values('vendas', ascending=True)
    fig_cat = px.bar(df_cat, x='vendas', y='Category', orientation='h',
                     title="Ranking de Vendas por Categoria",
                     color_discrete_sequence=[COR_AZUL_PRINCIPAL], template="plotly_dark")
    
    fig_cat.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_cat, use_container_width=True)

    # --- Gráfico 4: Volume de Compras (Linha Clean) ---
    df_qtd = df_selection.groupby('Season').size().reset_index(name='qtd')
    fig_qtd = px.line(df_qtd, x='Season', y='qtd', markers=True,
                      title="Volume de Compras (Tendência)", template="plotly_dark")
    
    fig_qtd.update_traces(line=dict(color=COR_AZUL_PRINCIPAL, width=4), 
                          marker=dict(color=COR_PONTOS_LINHA, size=10))
    
    fig_qtd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', 
                          yaxis=dict(gridcolor=COR_GRID), xaxis=dict(gridcolor=COR_GRID))
    st.plotly_chart(fig_qtd, use_container_width=True)

st.markdown("---")
st.caption("Dashboard atualizado com o padrão de cores solicitado.")