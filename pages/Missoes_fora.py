import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import api_gs.api_gs_missoes_fora_sede as api_gs
import models.tripulante as tripulantes


def gerar_grafico_missoes_fora_de_sede(data, missao):
    base = alt.Chart(data)
    new_chart = base.mark_bar(color='red',
                              opacity=0.9, ).encode(
        x=alt.X('Trigrama:N', sort='-y', title='', axis=alt.Axis(labelAngle=0)),
        y=alt.Y(f'sum({missao}):Q', title='Dias fora de sede'),
        color=alt.Color('Status',
                        scale=alt.Scale(
                            domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                            range=['#70c1ff', '#cccccc', '#8aeba6']
                        ), legend=alt.Legend(orient='top')),
        order=alt.Order('Status', sort='ascending')
    )
    return new_chart


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO - Outs',
                   page_icon=':airplane',
                   initial_sidebar_state='collapsed')


def carregar_dados_para_graficos(gs_data):
    gs_data['Ida'] = pd.to_datetime(gs_data['Ida'], format='%d/%m/%Y')
    gs_data['Volta'] = pd.to_datetime(gs_data['Volta'], format='%d/%m/%Y')

    gs_data['Dias fora de sede'] = gs_data['Volta'] - gs_data['Ida']
    gs_data['Dias fora de sede'] = gs_data['Dias fora de sede'].apply(
        lambda x: int(x.days) + 1)

    lista_trip = tripulantes.tripulantes_list
    todos_trigramas = set(map(lambda x: x.trigrama, lista_trip))

    trigramas_fora_sede = gs_data['Trigrama'].to_list()

    # Essa operação me dá uma lista com os trigramas que não ficaram fora de sede ainda
    trigramas_em_casa = list(todos_trigramas - set(trigramas_fora_sede))

    lista_de_none = []
    for i in range(len(trigramas_em_casa)):
        lista_de_none.append('')

    col_trigramas = trigramas_fora_sede + trigramas_em_casa
    col_missao = gs_data['Missão'].to_list() + lista_de_none
    col_ida = gs_data['Ida'].to_list() + lista_de_none
    col_volta = gs_data['Volta'].to_list() + lista_de_none
    col_status = gs_data['Status'].to_list() + lista_de_none
    col_verificado = gs_data['Verificado'].to_list() + lista_de_none
    col_dias_fora_sede = gs_data['Dias fora de sede'].to_list() + lista_de_none

    table = pd.DataFrame({'Trigrama': col_trigramas,
                          'Missão': col_missao,
                          'Ida': col_ida,
                          'Volta': col_volta,
                          'Status': col_status,
                          'Verificado': col_verificado,
                          'Dias fora de sede': col_dias_fora_sede})

    table['Dias fora de sede'] = table['Dias fora de sede'].replace('', 0)
    table['Missão'] = table['Missão'].replace('', 'Sem missão alocada')
    table['Ida'] = table['Ida'].replace('', 'Sem data prevista')
    table['Volta'] = table['Volta'].replace('', 'Sem volta prevista')

    return table


def carregar_dados_para_tabelas(gs_data):
    gs_data['Ida'] = pd.to_datetime(gs_data['Ida'], format='%d/%m/%Y')
    gs_data['Volta'] = pd.to_datetime(gs_data['Volta'], format='%d/%m/%Y')

    gs_data['Dias fora de sede'] = gs_data['Volta'] - gs_data['Ida']
    gs_data['Dias fora de sede'] = gs_data['Dias fora de sede'].apply(
        lambda x: int(x.days) + 1)

    return gs_data


missoes_fora_sede_graficos = carregar_dados_para_graficos(api_gs.main())
missoes_fora_sede_tabelas = carregar_dados_para_tabelas(gs_data=api_gs.main())

# Mostrando apenas a data
missoes_fora_sede_tabelas['Ida'] = missoes_fora_sede_tabelas['Ida'].apply(lambda x: x.date(), )
missoes_fora_sede_tabelas['Volta'] = missoes_fora_sede_tabelas['Volta'].apply(lambda x: x.date())

# Organizando os dados em wide-data - cada missão é uma coluna
pivot_table = pd.pivot_table(data=missoes_fora_sede_tabelas.reset_index(),
                             index=['Trigrama', 'Status'],
                             values='Dias fora de sede',
                             aggfunc=np.sum,
                             columns=['Missão'],
                             fill_value=0).reset_index()

# Conteúdo de apresentação da página
st.markdown('### Tabelas e Gráficos de missões fora sede :bar_chart:')
st.markdown('O objetivo dessa página:')
st.markdown(
    ' 1. Ser transparente com todos os militares quanto á quantos dias cada militar está ficando fora de sede.\n'
    '2. Facilitar o serviço da escala no momento de escalar um militar para missões fora de sede. ')
st.markdown(
    'Todos os dados aqui lançados são baseados na planilha de controle de missões fora de sede da CCIAO. '
    'Caso algum militar perceba alguma discrepância, '
    'favor avisar a CCIAO para que possamos ajustar o mais rápido possível e não trabalharmos com dados errados.')
st.markdown('**A fonte da maior parte das informações é baseada na FACD de cada militar.**')
st.markdown('***Dê preferência para visualizar os gráficos em uma tela de computador ao invés de celular. Devido ao'
            'tamanho da tela do celular pode ser que alguns dados sejam omitidos, se mesmo assim estiver '
            ' visualizando no celular, habilite o modo Desktop nas opções do seu navegador e coloque o celular'
            ' na posição horizontal..***')
# Dados gerais
if st.checkbox('Mostrar dados gerais'):
    col1, col2, col3 = st.columns(3)
    with col1:
        trigramas_selecionados = st.multiselect(label='Trigrama',
                                                options=missoes_fora_sede_tabelas['Trigrama'].unique())
    with col2:
        missoes_selecionadas = st.multiselect(label='Missão',
                                              options=missoes_fora_sede_tabelas['Missão'].unique())
    with col3:
        status_selecionados = st.multiselect(label='Status',
                                             options=missoes_fora_sede_tabelas['Status'].unique())

    # Se não filtrar nada é considerado que todos valores serão mostrados
    if len(trigramas_selecionados) == 0:
        trigramas_selecionados = list(missoes_fora_sede_tabelas['Trigrama'].unique())
    if len(missoes_selecionadas) == 0:
        missoes_selecionadas = list(missoes_fora_sede_tabelas['Missão'].unique())
    if len(status_selecionados) == 0:
        status_selecionados = list(missoes_fora_sede_tabelas['Status'].unique())
    # Aplicando filtros
    st.dataframe(missoes_fora_sede_tabelas.query("Trigrama == @trigramas_selecionados & "
                                                 "Missão == @missoes_selecionadas &"
                                                 "Status == @status_selecionados"), use_container_width=True)

if st.checkbox('Mostrar dados por missão'):
    st.dataframe(pivot_table, use_container_width=True)

# Gráficos
st.markdown('#### Amazônia :deciduous_tree:')
grafico_amazonia = gerar_grafico_missoes_fora_de_sede(data=pivot_table, missao='OPERAÇÃO YANOMAMI/AMAZÔNIA')
st.altair_chart(grafico_amazonia, use_container_width=True)

st.markdown('#### Missões COMPREP ICA 55-87 + Simulador')

initial_data = api_gs.main()
demais_missoes_table = carregar_dados_para_graficos(initial_data.loc[(initial_data['Missão'] == 'TÁPIO') |
                                                                     (initial_data['Missão'] == 'TÍNIA') |
                                                                     (initial_data['Missão'] == 'IVR') |
                                                                     (initial_data['Missão'] == 'SIMULADOR') |
                                                                     (initial_data['Missão'] == 'Sem missão alocada')])

base_comprep = alt.Chart(demais_missoes_table)
chart_comprep = base_comprep.mark_bar(opacity=0.9).encode(
    x=alt.X('Trigrama:N', sort='-y', axis=alt.Axis(labelAngle=0), title=''),
    y=alt.Y('sum(Dias fora de sede):Q'),
    color=alt.Color('Status',
                    scale=alt.Scale(
                        domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                        range=['#70c1ff', '#cccccc', '#8aeba6']
                    ), legend=alt.Legend(orient='top')
                    ),
    order=alt.Order('Status', sort='ascending')
)

st.altair_chart(chart_comprep, use_container_width=True)

st.markdown('#### Demais missões')
demais_missoes_table = carregar_dados_para_graficos(
    initial_data.loc[(initial_data['Missão'] != 'TÁPIO') &
                     (initial_data['Missão'] != 'OPERAÇÃO YANOMAMI/AMAZÔNIA') &
                     (initial_data['Missão'] != 'TÍNIA') &
                     (initial_data['Missão'] != 'IVR') &
                     (initial_data['Missão'] != 'SIMULADOR') &
                     (initial_data['Missão'] != 'Sem missão alocada')])

demais_missoes_chart = alt.Chart(demais_missoes_table).mark_bar(opacity=0.9).encode(
    x=alt.X('Trigrama:N', sort='-y', axis=alt.Axis(labelAngle=0), title=''),
    y=alt.Y('sum(Dias fora de sede):Q'),
    color=alt.Color('Status',
                    scale=alt.Scale(
                        domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                        range=['#70c1ff', '#cccccc', '#8aeba6']
                    )
                    , legend=alt.Legend(orient='top')),
    order=alt.Order('Status', sort='ascending'))

st.altair_chart(demais_missoes_chart, use_container_width=True)

# Gráfico total de dias fora de sede
base_chart = alt.Chart(missoes_fora_sede_graficos)
chart = base_chart.mark_bar(opacity=0.9).encode(
    x=alt.X('Trigrama:N', sort='-y', axis=alt.Axis(labelAngle=0), title=''),
    y=alt.Y('sum(Dias fora de sede):Q'),
    color=alt.Color('Status',
                    scale=alt.Scale(
                        domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                        range=['#70c1ff', '#cccccc', '#8aeba6']
                    ), legend=alt.Legend(orient='top')),
    order=alt.Order('Status', sort='ascending')
)

st.markdown('#### Total de dias fora de sede :baggage_claim:')
st.altair_chart(chart, use_container_width=True)
