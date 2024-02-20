import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import calendar
import locale
from data_handler import *
from PIL import Image
from datetime import datetime, timedelta
from streamlit_option_menu import option_menu

df, df_a, df_f, df_s, ultima_atualizacao = consulta()

# ----------------- PAG CONFIG ----------------- #
icon = Image.open('images/icon.png')
st.set_page_config(page_title='Helpdesk - Painel', layout="wide",
                   initial_sidebar_state='expanded', page_icon=icon)

# ----------------- STYLES ----------------- #
with open("style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# ----------------- SIDEBAR ----------------- #
st.sidebar.markdown(
    '<img src="app/static/Helpdesk.png" id="sidebar_icon">', unsafe_allow_html=True)

with st.sidebar:
    menu_selected = option_menu(None, ['Visão Geral', 'Em Andamento', 'SLA', 'Explorar'],
                                icons=['house', 'hourglass-split', 'stopwatch', 'search'], default_index=0,
                                styles={
        "container": {"background-color": "#061638", "padding": "0!important", "border-radius": "0px"},
        "nav-link": {"color": "white", "font-family": "'Open Sans', sans-serif"},
        "nav-link-selected": {"color": "#061638", "background-color": "white", "font-family": "'Open Sans', sans-serif"},
    })

end_date = datetime.today()
start_date = datetime(2020, 7, 1)

with st.sidebar.expander("Filtros"):
    # Filtro Favorito de Data
    dataf = ['HOJE', 'ESSE MÊS', 'MÊS ANTERIOR', 'ESSE ANO', 'SEMPRE']
    dataf_selec = st.selectbox("Data", dataf)
    if dataf_selec == 'HOJE':
        end_date = datetime.today()
        start_date = datetime.today()
    elif dataf_selec == 'ESSE MÊS':
        end_date = datetime.today()
        start_date = datetime(end_date.year, end_date.month, 1)
    elif dataf_selec == 'ESSE ANO':
        end_date = datetime.today()
        start_date = datetime(end_date.year, 1, 1)
    elif dataf_selec == 'MÊS ANTERIOR':
        start_date = datetime(end_date.year, end_date.month - 1, 1)
        end_date = datetime(end_date.year, end_date.month,
                            1) - timedelta(days=1)

    # Filtro de Data Inicial e Data Final
    from_date = st.date_input('Data inicial:', start_date)
    to_date = st.date_input('Data final:', end_date)
    df_a = df_a.query('ABERTURA >= @from_date and ABERTURA <= @to_date')
    df_s = df_s.query('DataSolucao >= @from_date and DataSolucao <= @to_date')
    df_f = df_f.query(
        'DataFechamento >= @from_date and DataFechamento <= @to_date')

    # Filtro de Técnicos
    tec = sorted((df['TECNICO'].value_counts().index).tolist())
    tec.insert(0, 'TODOS')
    tec_selec = st.selectbox("Técnico:", tec)
    if tec_selec != 'TODOS':
        df_s = df_s.query("TECNICO == @tec_selec")
        df_a = df_a.query("TECNICO == @tec_selec")
        df_f = df_f.query("TECNICO == @tec_selec")

    # Filtro de Localização
    loca = sorted((df['LOCALIZACAO'].value_counts().index).tolist())
    loca.insert(0, 'TODOS')
    loca_selec = st.selectbox("Setor:", loca)
    if loca_selec != 'TODOS':
        df_s = df_s.query("LOCALIZACAO == @loca_selec")
        df_a = df_a.query("LOCALIZACAO == @loca_selec")
        df_f = df_f.query("LOCALIZACAO == @loca_selec")

    # Filtro de Requerentes
    req = sorted((df['REQUERENTE'].value_counts().index).tolist())
    req.insert(0, 'TODOS')
    req_selec = st.selectbox("Requerente:", req)
    if req_selec != 'TODOS':
        df_s = df_s.query("REQUERENTE == @req_selec")
        df_a = df_a.query("REQUERENTE == @req_selec")
        df_f = df_f.query("REQUERENTE == @req_selec")

    # Filtro de Organização
    org = (df['ORGANIZACAO'].value_counts().index).tolist()
    org_selec = st.multiselect('Organização', options=org, default=org)
    df_s = df_s.query("ORGANIZACAO == @org_selec")
    df_a = df_a.query("ORGANIZACAO == @org_selec")
    df_f = df_f.query("ORGANIZACAO == @org_selec")

    # Filtro de Grupo
    grp = sorted((df['GRUPO'].value_counts().index).tolist())
    grp_selec = st.multiselect('Grupo', options=grp, default=grp)
    df_s = df_s.query("GRUPO == @grp_selec")
    df_a = df_a.query("GRUPO == @grp_selec")
    df_f = df_f.query("GRUPO == @grp_selec")

    # Filtro de Situação
    situ = sorted((df['SITUACAO'].value_counts().index).tolist())
    situ_selec = st.multiselect('Situação', options=situ, default=situ)
    df_s = df_s.query("SITUACAO == @situ_selec")
    df_a = df_a.query("SITUACAO == @situ_selec")
    df_f = df_f.query("SITUACAO == @situ_selec")

    # Filtro de Tipo de Solução
    tsol = sorted((df['TIPO_SOLUCAO'].value_counts().index).tolist())
    tsol_selec = st.multiselect(
        'Tipo de Solução', options=tsol, default=tsol)
    df_s = df_s.query("TIPO_SOLUCAO == @tsol_selec")
    df_f = df_f.query("TIPO_SOLUCAO == @tsol_selec")

    # Filtro de Categoria 1
    cat1 = sorted((df['CATEGORIA'].value_counts().index).tolist())
    cat1.insert(0, 'TODAS')
    cat1_selec = st.selectbox("Categoria - N1:", cat1)
    if cat1_selec != 'TODAS':
        df_s = df_s.query("CATEGORIA == @cat1_selec")
        df_a = df_a.query("CATEGORIA == @cat1_selec")
        df_f = df_f.query("CATEGORIA == @cat1_selec")

    # Filtro de Categoria 2
    cat2 = sorted((df['CATEGORIA_2'].value_counts().index).tolist())
    cat2.insert(0, 'TODAS')
    cat2_selec = st.selectbox("Categoria - N2:", cat2)
    if cat2_selec != 'TODAS':
        df_s = df_s.query("CATEGORIA_2 == @cat2_selec")
        df_a = df_a.query("CATEGORIA_2 == @cat2_selec")
        df_f = df_f.query("CATEGORIA_2 == @cat2_selec")

    # Filtro de Categoria 3
    cat3 = sorted((df['CATEGORIA_3'].value_counts().index).tolist())
    cat3.insert(0, 'TODAS')
    cat3_selec = st.selectbox("Categoria - N3:", cat3)
    if cat3_selec != 'TODAS':
        df_s = df_s.query("CATEGORIA_3 == @cat3_selec")
        df_a = df_a.query("CATEGORIA_3 == @cat3_selec")
        df_f = df_f.query("CATEGORIA_3 == @cat3_selec")

    if st.button('Atualizar'):
        df, df_a, df_f, df_s, ultima_atualizacao = consulta()
    #   st.experimental_rerun()
    st.markdown(f'##### Última atualização: {ultima_atualizacao}')

# ----------------- VARIAVEIS ----------------- #
df_solu_vw = df_s.loc[:, ["ABERTURA", "DataSolucao", "DataFechamento", "TECNICO", "REQUERENTE", "CHAMADO", "CATEGORIA", "CATEGORIA_2", "TIPO_SOLUCAO", "LOCALIZACAO", "SITUACAO", "STATUS_SLA", "URL_TICKET"]]
df_solu_vw = df_solu_vw.rename(columns={'ABERTURA': 'Data de Abertura', 'DataSolucao': 'Data de Solução', 'DataFechamento': 'Data de Fechamento', 'TECNICO': 'Técnico', 'REQUERENTE': 'Requerente', 'CHAMADO': 'Nº Chamado', 'STATUS_SLA': 'Status SLA',
                                      'TIPO_SOLUCAO': 'Tipo de Solução', 'LOCALIZACAO': 'Localização', 'SITUACAO': 'Situação', 'URL_TICKET': 'URL do Chamado', 'CATEGORIA': 'Categoria Nível 1', 'CATEGORIA_2': 'Categoria Nível 2'})
df_solu_vw = df_solu_vw.reindex(columns=['Nº Chamado', 'Data de Abertura', 'Requerente', 'Localização', 'Categoria Nível 1', 'Categoria Nível 2',
                                       'Técnico', 'Data de Solução', 'Tipo de Solução', 'Situação', 'Data de Fechamento', 'URL do Chamado', 'Status SLA'])
df_solu_vw = df_solu_vw.reset_index(drop=True)
df_solu_vw.index += 1

df_aber_vw = df_a.loc[:, ["ABERTURA", "DataSolucao", "DataFechamento", "TECNICO", "REQUERENTE", "CHAMADO", "CATEGORIA", "CATEGORIA_2", "TIPO_SOLUCAO", "LOCALIZACAO", "SITUACAO", "STATUS_SLA", "URL_TICKET"]]
df_aber_vw = df_aber_vw.rename(columns={'ABERTURA': 'Data de Abertura', 'DataSolucao': 'Data de Solução', 'DataFechamento': 'Data de Fechamento', 'TECNICO': 'Técnico', 'REQUERENTE': 'Requerente', 'CHAMADO': 'Nº Chamado', 'STATUS_SLA': 'Status SLA',
                                      'TIPO_SOLUCAO': 'Tipo de Solução', 'LOCALIZACAO': 'Localização', 'SITUACAO': 'Situação', 'URL_TICKET': 'URL do Chamado', 'CATEGORIA': 'Categoria Nível 1', 'CATEGORIA_2': 'Categoria Nível 2'})
df_aber_vw = df_aber_vw.reindex(columns=['Nº Chamado', 'Data de Abertura', 'Requerente', 'Localização', 'Categoria Nível 1', 'Categoria Nível 2',
                                       'Técnico', 'Data de Solução', 'Tipo de Solução', 'Situação', 'Data de Fechamento', 'URL do Chamado', 'Status SLA'])
df_aber_vw = df_aber_vw.reset_index(drop=True)
df_aber_vw.index += 1

df_em_and_vw = df.loc[:, ["ABERTURA", "TECNICO", "REQUERENTE", "CHAMADO", "CATEGORIA", "CATEGORIA_2", "LOCALIZACAO", "SITUACAO", "URL_TICKET"]]
df_em_and_vw = df_em_and_vw.rename(columns={'ABERTURA': 'Data de Abertura', 'TECNICO': 'Técnico', 'REQUERENTE': 'Requerente', 'CHAMADO': 'Nº Chamado',
                                      'LOCALIZACAO': 'Localização', 'SITUACAO': 'Situação', 'URL_TICKET': 'URL do Chamado', 'CATEGORIA': 'Categoria Nível 1', 'CATEGORIA_2': 'Categoria Nível 2'})
df_em_and_vw = df_em_and_vw.reindex(columns=['Nº Chamado', 'Data de Abertura', 'Requerente', 'Localização', 'Categoria Nível 1', 'Categoria Nível 2',
                                       'Técnico', 'Situação', 'URL do Chamado'])
df_em_and_vw = df_em_and_vw.reset_index(drop=True)
df_em_and_vw.index += 1

df_em_aberto = df_em_and_vw.loc[df_em_and_vw['Situação'] == 'ABERTO']
df_em_aberto = df_em_aberto.drop('Situação', axis=1).reset_index(drop=True)
df_em_aberto.index += 1

df_pendente = df_em_and_vw.loc[df_em_and_vw['Situação'] == 'PENDENTE']
df_pendente = df_pendente.drop('Situação', axis=1).reset_index(drop=True)
df_pendente.index += 1

df_atrasados = df_solu_vw.loc[df_solu_vw['Status SLA'] == 'ATRASADO']
df_atrasados = df_atrasados.drop(['Status SLA', 'Data de Fechamento'], axis=1).reset_index(drop=True)
df_atrasados.index += 1

total_abertos = df_a.shape[0]

try:
    total_em_aberto = df['SITUACAO'].value_counts()['ABERTO']
except KeyError as e:
    total_em_aberto = 0

try:
    total_pendentes = df['SITUACAO'].value_counts()['PENDENTE']
except KeyError as e:
    total_pendentes = 0

total_solucionados = df_s.shape[0]

try:
    total_fechados = df_f['SITUACAO'].value_counts()['FECHADO']
except KeyError as e:
    total_fechados = 0

try:
    total_excluidos = df['SITUACAO'].value_counts()['EXCLUIDO']
except KeyError as e:
    total_excluidos = 0

# ----------------- FIGURAS ----------------- #

# Fig 1 - Solucionados por Grupo
df1 = df_s['GRUPO'].value_counts()
porcentagem1 = df1 / df_s.shape[0] * 100

fig1 = go.Figure()
fig1.add_bar(x=df_s['GRUPO'].value_counts().index,
             y=df1,
             marker_color=['#0068c9', '#83c9ff'],
             hovertemplate='<br><b>Chamados Solucionados:</b> %{y}<extra></extra>',
             text=[f'{p:.2f}%' for p in porcentagem1])

fig1.update_layout(xaxis_tickangle=0,
                   xaxis={'title': None, 'fixedrange': True},
                   yaxis={'title': None, 'fixedrange': True},
                   font_family='Open Sans',
                   legend_title_text="GRUPO",
                   legend_itemclick=False,
                   legend_itemdoubleclick=False)

# Fig 2 - Solucionados por Status SLA
df2 = df_s['STATUS_SLA'].value_counts()
fig2 = go.Figure()
fig2.add_trace(go.Pie(labels=df_s['STATUS_SLA'].value_counts().index,
                      values=df2,
                      hole=.6,
                      hovertemplate='<br><b>Status:</b> %{label}' +
                      '<br><b>Chamados Solucionados:</b> %{value}' +
                                    '<br><b>Porcentagem:</b> %{percent}<extra></extra>'))

fig2.update_layout(uniformtext_minsize=12,
                   uniformtext_mode='hide',
                   font_family='Open Sans',
                   legend_title_text="SLA",
                   legend_itemclick=False,
                   legend_itemdoubleclick=False)

# Fig 3 - Solucionados por Tipo de Solução
df3 = df_s['TIPO_SOLUCAO'].value_counts()
fig3 = go.Figure()
fig3.add_trace(go.Pie(labels=df3.index,
                      values=df3,
                      hole=.6,
                      textposition='inside',
                      hovertemplate='<br><b>Tipo de Solução:</b> %{label}' +
                      '<br><b>Chamados Solucionados:</b> %{value}' +
                                    '<br><b>Porcentagem:</b> %{percent}<extra></extra>'))

fig3.update_layout(uniformtext_minsize=12,
                   uniformtext_mode='hide',
                   font_family='Open Sans',
                   legend_title_text="TIPO DE SOLUÇÃO",
                   legend_itemclick='toggle',
                   legend_itemdoubleclick=False)

# Fig 4 - Solucionados por Local
df4 = df_s['LOCALIZACAO'].value_counts()
fig4 = go.Figure()
fig4.add_trace(go.Pie(labels=df4.index,
                      values=df4,
                      hole=.6,
                      textposition='inside',
                      hovertemplate='<br><b>Localização:</b> %{label}' +
                      '<br><b>Chamados Solucionados:</b> %{value}' +
                                    '<br><b>Porcentagem:</b> %{percent}<extra></extra>'))

fig4.update_layout(uniformtext_minsize=12,
                   uniformtext_mode='hide',
                   font_family='Open Sans',
                   legend_title_text="LOCALIZAÇÃO",
                   legend_itemclick='toggle',
                   legend_itemdoubleclick=False)

# Fig 5 - Solucionados por Técnico
df5 = df_s['TECNICO'].value_counts().iloc[::-1]
fig5 = go.Figure()
fig5.add_trace(go.Bar(x=df5,
                      y=df5.index,
                      orientation='h',
                      text=df5))

fig5.update_layout(xaxis={'title': None, 'fixedrange': True},
                   yaxis={'title': None, 'fixedrange': True},
                   font_family='Open Sans',
                   hovermode=False)

# Fig 6  - Solucionados por Técnico por Mês
df6 = df_s.groupby(['MesAnoSolucao', 'TECNICO'])[
    'CHAMADO'].count().reset_index()
df6_group = df_s.groupby('MesAnoSolucao')['CHAMADO'].count().reset_index()
fig6 = go.Figure()
fig6 = px.line(df6,
               x='MesAnoSolucao',
               y='CHAMADO',
               color='TECNICO')

fig6.update_traces(hovertemplate='<br><b>Mês da Solução:</b> %{x}' +
                   '<br><b>Chamados Solucionados:</b> %{y}')

fig6.update_layout(xaxis={'title': 'Mês de Solução', 'fixedrange': True},
                   yaxis={'title': 'Chamados Solucionados', 'fixedrange': True},
                   legend_itemclick='toggleothers',
                   font_family='Open Sans',
                   legend_title_text="TÉCNICO")

# Fig 7 - Solucionados por Técnico por Dia
df7 = df_s.groupby(['DataSolucao', 'TECNICO'])['CHAMADO'].count().reset_index()
df7_group = df_s.groupby('DataSolucao')['CHAMADO'].count().reset_index()
fig7 = go.Figure()
fig7 = px.line(df7,
               x='DataSolucao',
               y='CHAMADO',
               color='TECNICO')

fig7.update_traces(hovertemplate='<br><b>Dia da Solução:</b> %{x}' +
                   '<br><b>Chamados Solucionados:</b> %{y}')

fig7.update_layout(xaxis={'title': 'Dia da Solução', 'fixedrange': True},
                   yaxis={'title': 'Chamados Solucionados', 'fixedrange': True},
                   legend_itemclick='toggleothers',
                   font_family='Open Sans',
                   legend_title_text="TÉCNICO")

### Fig 10 - Em andamento por técnico
####--ORIGINAL--##
##df10 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO')]
##
##df10 = df10[['TECNICO', 'SITUACAO']]
##df10_grouped = df10.groupby(
##    ['TECNICO', 'SITUACAO']).size().reset_index(name='count')
##df10_pivot = df10_grouped.pivot(
##    index='TECNICO', columns='SITUACAO', values='count')
##df10_pivot = df10_pivot.reset_index()
##
####--ORIGINAL--##
##df10_pivot[['ABERTO', 'PENDENTE']] = df10_pivot[['ABERTO', 'PENDENTE']].fillna(0)
##df10_pivot['SOMA'] = df10_pivot['ABERTO'] + df10_pivot['PENDENTE']
##
##df10_pivot_sorted = df10_pivot.sort_values('SOMA', ascending=False)
##df10_pivot_sorted = df10_pivot_sorted.dropna(subset=['SOMA'])
##df10_pivot_sorted['SOMA'] = df10_pivot_sorted['SOMA'].astype(int)
##df10_pivot_sorted = df10_pivot_sorted.sort_values(by='SOMA', ascending=True)
##
##fig10 = go.Figure()
##fig10 = px.bar(df10_pivot_sorted,
##               x=['ABERTO', 'PENDENTE'],
##               y='TECNICO',
##               orientation='h',
##               barmode='stack',
##               text_auto=True)
##
##fig10.update_traces(hovertemplate='%{x}')
##
##fig10.update_layout(xaxis={'title': None, 'fixedrange': True},
##                    yaxis={'title': None, 'fixedrange': True},
##                    font_family='Open Sans',
##                    legend_title_text="SITUAÇÃO",
##                    legend_itemclick='toggleothers')

### Fig 10 - Em andamento por técnico ###--- TESTE EXCLUIDOS --###

##--ORIGINAL--##
df10 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO')]


#df10 = df[df['SITUACAO'].isin(['ABERTO', 'PENDENTE'])]
#df10 = df[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO') | (df['SITUACAO'] == 'EXCLUIDO')]
#df10 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO') | (df['SITUACAO'] != 'EXCLUIDO')]

df10 = df10[['TECNICO', 'SITUACAO']]
df10_grouped = df10.groupby(
    ['TECNICO', 'SITUACAO']).size().reset_index(name='count')
df10_pivot = df10_grouped.pivot(
    index='TECNICO', columns='SITUACAO', values='count')
df10_pivot = df10_pivot.reset_index()

####-- TETE EXCLUIDOS --##
##df10 = df.loc[(df['SITUACAO'] == 'EXCLUIDO')]
##df10_pivot[['EXCLUIDO']] = df10_pivot[['EXCLUIDO']].fillna(0)
##df10_pivot['SOMA'] = df10_pivot['EXCLUIDO'] + df10_pivot['EXCLUIDO']

##--ORIGINAL--##
df10_pivot[['ABERTO', 'PENDENTE']] = df10_pivot[['ABERTO', 'PENDENTE']].fillna(0)
df10_pivot['SOMA'] = df10_pivot['ABERTO'] + df10_pivot['PENDENTE']

#df10_pivot[['ABERTO', 'PENDENTE', 'EXCLUIDO']] = df10_pivot[['ABERTO', 'PENDENTE', 'EXCLUIDO']].fillna(0)
#df10_pivot['SOMA'] = df10_pivot['ABERTO'] + df10_pivot['PENDENTE'] - df10_pivot['EXCLUIDO']

df10_pivot_sorted = df10_pivot.sort_values('SOMA', ascending=False)
df10_pivot_sorted = df10_pivot_sorted.dropna(subset=['SOMA'])
df10_pivot_sorted['SOMA'] = df10_pivot_sorted['SOMA'].astype(int)
df10_pivot_sorted = df10_pivot_sorted.sort_values(by='SOMA', ascending=True)

fig10 = go.Figure()
fig10 = px.bar(df10_pivot_sorted,
               x=['ABERTO', 'PENDENTE'],
               y='TECNICO',
               orientation='h',
               barmode='stack',
               text_auto=True)

fig10.update_traces(hovertemplate='%{x}')

fig10.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    legend_title_text="SITUAÇÃO",
                    legend_itemclick='toggleothers')
### FIM -Fig 10 - Em andamento por técnico ###--- TESTE EXCLUIDOS --###

# Fig 11 - Em andamento por requerente
df11 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO')]
df11 = df11[['REQUERENTE', 'SITUACAO']]
df11_grouped = df11.groupby(
    ['REQUERENTE', 'SITUACAO']).size().reset_index(name='count')
df11_pivot = df11_grouped.pivot(
    index='REQUERENTE', columns='SITUACAO', values='count').reset_index()
df11_pivot[['ABERTO', 'PENDENTE']] = df11_pivot[[
    'ABERTO', 'PENDENTE']].fillna(0)
df11_pivot['SOMA'] = df11_pivot['ABERTO'] + df11_pivot['PENDENTE']
df11_pivot_sorted = df11_pivot.sort_values('SOMA', ascending=False)
df11_pivot_sorted = df11_pivot_sorted.dropna(subset=['SOMA'])
df11_pivot_sorted['SOMA'] = df11_pivot_sorted['SOMA'].astype(int)
df11_pivot_sorted = df11_pivot_sorted.sort_values(by='SOMA', ascending=True)
df11_pivot_sorted = df11_pivot_sorted.tail(10)

fig11 = go.Figure()
fig11 = px.bar(df11_pivot_sorted,
               x=['ABERTO', 'PENDENTE'],
               y='REQUERENTE',
               orientation='h',
               barmode='stack',
               text_auto=True)

fig11.update_traces(hovertemplate='%{x}')

fig11.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    legend_title_text="SITUAÇÃO",
                    legend_itemclick='toggleothers')

# Fig 12 - Chamados Abertos x Solucionados por Mês
df_abertos_mes = df_a.groupby('MesAnoAbertura')[
    'CHAMADO'].count().reset_index()
df_solucionados_mes = df_s.groupby('MesAnoSolucao')[
    'CHAMADO'].count().reset_index()

fig12 = go.Figure()
fig12.add_trace(go.Scatter(y=df_abertos_mes['CHAMADO'],
                           x=df_abertos_mes['MesAnoAbertura'],
                           mode='lines+markers',
                           name='ABERTOS')
                )

fig12.add_trace(go.Scatter(y=df_solucionados_mes['CHAMADO'],
                           x=df_solucionados_mes['MesAnoSolucao'],
                           mode='lines+markers',
                           name='SOLUCIONADOS')
                )

fig12.update_traces(hovertemplate='<br><b>Mês:</b> %{x}' +
                    '<br><b>Chamados:</b> %{y}')

fig12.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    legend_title_text="CHAMADOS",
                    legend_itemclick='toggleothers')

# Fig 13 - Status SLA pelo tempo
df13 = df.dropna(subset=['DataSolucao'])
df13['MesAnoSolucao'] = df13['DataSolucao'].apply(
    lambda x: x.replace(day=calendar.monthrange(x.year, x.month)[1]))
df13 = df13.dropna(subset=['MesAnoSolucao'])
df13_group = df13.copy()
df13_group = df13.groupby('MesAnoSolucao')['STATUS_SLA'].value_counts(
    normalize=True).loc[:, 'NO PRAZO']*100

fig13 = go.Figure()
fig13 = px.line(df13_group,
                x=df13_group.index,
                y=df13_group)

fig13.add_shape(type="line",
                x0=df13_group.index[0],
                y0=99,
                x1=df13_group.index[-1],
                y1=99,
                line=dict(color='red', width=2, dash='dot'))

fig13.update_traces(hovertemplate='<br><b>Mês da Solução:</b> %{x}' +
                    '<br><b>Indicador SLA:</b> %{y}%')

fig13.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    legend_itemclick='toggleothers',
                    font_family='Open Sans')

# Fig 14 - Chamados Abertos x Solucionados por Dia
df_abertos_dia = df_a.groupby('ABERTURA')['CHAMADO'].count().reset_index()
df_solucionados_dia = df_s.groupby(
    'DataSolucao')['CHAMADO'].count().reset_index()

fig14 = go.Figure()
fig14.add_trace(go.Scatter(y=df_abertos_dia['CHAMADO'],
                           x=df_abertos_dia['ABERTURA'],
                           mode='lines+markers',
                           name='ABERTOS')
                )

fig14.add_trace(go.Scatter(y=df_solucionados_dia['CHAMADO'],
                           x=df_solucionados_dia['DataSolucao'],
                           mode='lines+markers',
                           name='SOLUCIONADOS')
                )

fig14.update_traces(hovertemplate='<br><b>Dia:</b> %{x}' +
                    '<br><b>Chamados:</b> %{y}')

fig14.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    legend_title_text="CHAMADOS",
                    legend_itemclick='toggleothers')

# Fig 15 - Categoria - Nível 3
df15 = df_s['CATEGORIA_3'].value_counts()
df15 = df15.head(10)

fig15 = go.Figure()
fig15.add_trace(go.Pie(labels=df15.index,
                       values=df15,
                       hole=.6,
                       hovertemplate='<br><b>Categoria N3:</b> %{label}' +
                       '<br><b>Chamados Solucionados:</b> %{value}<extra></extra>'))

fig15.update_layout(uniformtext_minsize=12,
                    uniformtext_mode='hide',
                    font_family='Open Sans',
                    legend_title_text="CATEGORIAS N3 - TOP 10",
                    legend_itemclick='toggle',
                    legend_itemdoubleclick=False)

# Fig 17 - Categoria - Nível 1
df17 = df_s['CATEGORIA'].value_counts()
df17 = df17.head(10).iloc[::-1]

porcentagem17 = df17 / df17.sum() * 100
fig17 = go.Figure()
fig17.add_trace(go.Bar(x=df17,
                       y=df17.index,
                       orientation='h',
                       marker_color=px.colors.qualitative.Plotly,
                       hovertemplate='<br><b>Chamados:</b> %{x}<extra></extra>',
                       text=[f'{p:.2f}%' for p in porcentagem17]))

fig17.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans')


# Fig 18 - Chamados Abertos - Comparação Anual
df18 = df_a.groupby('MesAnoAbertura')['CHAMADO'].count().reset_index()
df18['MesAnoAbertura'] = pd.to_datetime(df18['MesAnoAbertura'])
df18['Ano'] = df18['MesAnoAbertura'].dt.year
df18['Mês'] = df18['MesAnoAbertura'].dt.month
df18.drop('MesAnoAbertura', axis=1, inplace=True)

fig18 = go.Figure()
fig18 = px.line(df18,
                x='Mês',
                y='CHAMADO',
                color='Ano')

fig18.update_traces(hovertemplate='<br><b>Mês:</b> %{x}' +
                    '<br><b>Chamados Abertos:</b> %{y}')

fig18.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    legend_itemclick='toggle',
                    font_family='Open Sans',
                    legend_title_text="ANO")

# Fig 19 - Chamados Solucionados - Comparação Anual
df19 = df_s.groupby('MesAnoSolucao')['CHAMADO'].count().reset_index()
df19['MesAnoSolucao'] = pd.to_datetime(df19['MesAnoSolucao'])
df19['Ano'] = df19['MesAnoSolucao'].dt.year
df19['Mês'] = df19['MesAnoSolucao'].dt.month
df19.drop('MesAnoSolucao', axis=1, inplace=True)

fig19 = go.Figure()
fig19 = px.line(df19,
                x='Mês',
                y='CHAMADO',
                color='Ano')

fig19.update_traces(hovertemplate='<br><b>Mês:</b> %{x}' +
                    '<br><b>Chamados Solucionados:</b> %{y}')

fig19.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    legend_itemclick='toggle',
                    font_family='Open Sans',
                    legend_title_text="ANO")

# Fig 20 - Status SLA por Requerente
df20 = df[['REQUERENTE', 'STATUS_SLA']]
df20_grouped = df20.groupby(
    ['REQUERENTE', 'STATUS_SLA']).size().reset_index(name='count')
df20_pivot = df20_grouped.pivot(
    index='REQUERENTE', columns='STATUS_SLA', values='count').reset_index()
df20_pivot[['ATRASADO', 'NO PRAZO']] = df20_pivot[[
    'ATRASADO', 'NO PRAZO']].fillna(0)
df20_pivot['SOMA'] = df20_pivot['ATRASADO'] + df20_pivot['NO PRAZO']
df20_pivot_sorted = df20_pivot.sort_values('SOMA', ascending=False)
df20_pivot_sorted = df20_pivot_sorted.dropna(subset=['SOMA'])
df20_pivot_sorted['SOMA'] = df20_pivot_sorted['SOMA'].astype(int)
df20_pivot_sorted = df20_pivot_sorted.sort_values(by='SOMA', ascending=True)
df20_pivot_sorted = df20_pivot_sorted.tail(10)

fig20 = px.bar(df20_pivot_sorted,
               x=['NO PRAZO', 'ATRASADO'],
               y='REQUERENTE',
               orientation='h',
               barmode='stack')

fig20.update_traces(hovertemplate='%{x}')

fig20.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    legend_title_text="SLA",
                    legend_itemclick='toggleothers')

# Fig 21 - Atribuídos ou Pendentes por Organização
df21 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO')]
df21 = df21['ORGANIZACAO'].value_counts()

porcentagem21 = df21 / df21.sum() * 100

fig21 = go.Figure()
fig21.add_bar(x=df21.index,
              y=df21,
              marker_color=['#0068c9', '#7defa1', '#ffd06a'],
              hovertemplate='<br><b>Chamados:</b> %{y}<extra></extra>',
              text=[f'{p:.2f}%' for p in porcentagem21])

fig21.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    xaxis_tickangle=0,
                    font_family='Open Sans',
                    legend_title_text="ORGANIZAÇÃO",
                    legend_itemclick=False,
                    legend_itemdoubleclick=False)


# Fig 22 - Atribuídos ou Pendentes por Setor
df22 = df.loc[(df['SITUACAO'] == 'PENDENTE') | (df['SITUACAO'] == 'ABERTO')]
df22 = df22[['LOCALIZACAO']].value_counts()

fig22 = go.Figure()
fig22.add_trace(go.Pie(labels=df22.index,
                       values=df22,
                       hole=.6,
                       hovertemplate='<br><b>Localização:</b> %{label}' +
                       '<br><b>Chamados:</b> %{value}' +
                       '<br><b>Porcentagem:</b> %{percent}<extra></extra>'))

fig22.update_layout(uniformtext_minsize=12,
                    uniformtext_mode='hide',
                    font_family='Open Sans',
                    legend_title_text="SLA",
                    legend_itemclick=False,
                    legend_itemdoubleclick=False)

# Fig 23 - Solucionados por Organização
df23 = df_s['ORGANIZACAO'].value_counts()

marker_color = ['#0068c9', '#7defa1', '#ffd06a']
porcentagem23 = df23 / df23.sum() * 100

fig23 = go.Figure()
fig23.add_bar(x=df23.index,
              y=df23,
              marker_color=['#0068c9', '#7defa1', '#ffd06a'],
              hovertemplate='<br><b>Chamados:</b> %{y}<extra></extra>',
              text=[f'{p:.2f}%' for p in porcentagem23])

fig23.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    xaxis_tickangle=0,
                    font_family='Open Sans',
                    legend_title_text="ORGANIZAÇÃO",
                    legend_itemclick=False,
                    legend_itemdoubleclick=False)

# Fig 24 - Solucionados por Requerente
df24 = df_s['REQUERENTE'].value_counts().head(10).iloc[::-1]

fig24 = go.Figure()
fig24.add_trace(go.Bar(x=df24,
                       y=df24.index,
                       orientation='h',
                       text=df24))

fig24.update_layout(xaxis={'title': None, 'fixedrange': True},
                    yaxis={'title': None, 'fixedrange': True},
                    font_family='Open Sans',
                    hovermode=False)

locale.setlocale(locale.LC_TIME, '')
mes_atual = calendar.month_name[int(datetime.now().strftime('%m'))]

df_sla = pd.DataFrame(df13_group)

sla_mes_atual = df_sla.iloc[-1, -1]
sla_mes_anterior = df_sla.iloc[-2, -1]
sla_delta = sla_mes_atual - sla_mes_anterior

sla_mes_atual = str("{:.2%}".format(sla_mes_atual/100))
sla_delta = str("{:.2%}".format(sla_delta/100))

# Atrasados do Mes Atual
df_qtd_atrasados_mes = df13.groupby('MesAnoSolucao')[
    'STATUS_SLA'].value_counts().loc[:, 'ATRASADO']
df_qtd_atrasados_mes = pd.DataFrame(df_qtd_atrasados_mes)

qtd_atrasados_mes_atual = df_qtd_atrasados_mes.iloc[-1, -1]
qtd_atrasados_mes_anterior = df_qtd_atrasados_mes.iloc[-2, -1]
qtd_atrasados_delta = qtd_atrasados_mes_atual - qtd_atrasados_mes_anterior

qtd_atrasados_mes_atual = str(qtd_atrasados_mes_atual)
qtd_atrasados_delta = str(qtd_atrasados_delta)


# ----------------- CORPO ----------------- #
if menu_selected == 'Visão Geral':
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric(label="Em Aberto", value=total_em_aberto)
    with col2:
        st.metric(label="Pendentes", value=total_pendentes)
    with col3:
        st.metric(label="Total Abertos", value=total_abertos)
    with col4:
        st.metric(label="Total Solucionados", value=total_solucionados)
    with col5:
        st.metric(label="Total Fechados", value=total_fechados)
    with col6:
        st.metric(label="Total Excluídos", value=total_excluidos)

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### Solucionados por Técnico")
        st.plotly_chart(fig5, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Solucionados por Grupo")
        st.plotly_chart(fig1, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("#### Solucionados por Requerente")
        st.plotly_chart(fig24, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Solucionados por Organização")
        st.plotly_chart(fig23, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Solucionados por Tipo de Setor")
        st.plotly_chart(fig4, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Solucionados por Tipo de Solução")
        st.plotly_chart(fig3, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns([100, 1])
    with col1:
        st.markdown("#### Solucionados por Categoria (N1)")
        st.plotly_chart(fig17, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Chamados solucionados por técnico")
        visu_data = st.radio('Visualizar por:',
                             ('Por dia', 'Por Mês'), horizontal=True)
        if visu_data == 'Por Mês':
            st.plotly_chart(fig6, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})
        else:
            st.plotly_chart(fig7, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns([100, 1])
    with col1:
        st.markdown("#### Abertos x Solucionados")
        visu_data = st.radio('Visualizar por: ',
                             ('Por dia', 'Por Mês'), horizontal=True)
        if visu_data == 'Por Mês':
            st.plotly_chart(fig12, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})
        else:
            st.plotly_chart(fig14, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Visão Mensal de Chamados")
        visu_data = st.radio('Visualizar:',
                             ('Abertos', 'Solucionados'), horizontal=True)
        if visu_data == 'Abertos':
            st.plotly_chart(fig18, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})
        else:
            st.plotly_chart(fig19, use_container_width=True,
                            theme='streamlit', config={'displayModeBar': False})


elif menu_selected == 'Em Andamento':
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Em Andamento por Técnico")
        st.plotly_chart(fig10, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Em Andamento por Requerente")
        st.plotly_chart(fig11, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Em Andamento por Organização")
        st.plotly_chart(fig21, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Em Andamento por Setor")
        st.plotly_chart(fig22, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})

    col1, col2 = st.columns([100, 1])
    with col1:
        st.markdown("#### Chamados Em Aberto")
        st.markdown("#### ")
        st.write(df_em_aberto)
    with col2:
        st.markdown("#### Chamados Pendentes")
        st.markdown("#### ")
        st.write(df_pendente)

elif menu_selected == 'SLA':
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f'SLA de {mes_atual}',
                  value=sla_mes_atual,
                  delta=sla_delta)
    with col2:
        st.metric(label=f'Chamados Atrasados em {mes_atual}',
                  value=qtd_atrasados_mes_atual,
                  delta=qtd_atrasados_delta,
                  delta_color="inverse")
    col1, col2 = st.columns([100, 1])
    with col1:
        st.markdown("#### Porcentagem de chamados dentro do prazo SLA por mês")
        st.plotly_chart(fig13, use_container_width=True,
                        theme='streamlit', config={'displayModeBar': False})
    with col2:
        st.markdown("#### Chamados Atrasados")
        st.markdown("##### ")
        st.write(df_atrasados)

elif menu_selected == 'Explorar':
    explorar = ['DATA DE SOLUÇÃO', 'DATA DE ABERTURA']
    explorar_selec = st.selectbox("Filtrar por", explorar)
    if explorar_selec == 'DATA DE SOLUÇÃO':
        st.write(df_solu_vw)
    elif explorar_selec == 'DATA DE ABERTURA':
        st.write(df_aber_vw)
