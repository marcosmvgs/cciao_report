import pandas as pd
import streamlit as st
import altair as alt
import numpy as np
import models.tripulante
import api_gs.api_gs_missoes_fora_sede as api_gs


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
                        )),
        order=alt.Order('Status', sort='ascending')
    )
    return new_chart


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO - Outs',
                   page_icon=':airplane')

# Carregando dados brutos
missoes_fora_sede_rawdata = api_gs.main()

missoes_fora_sede_rawdata['Ida'] = pd.to_datetime(missoes_fora_sede_rawdata['Ida'], format='%d/%m/%Y')
missoes_fora_sede_rawdata['Volta'] = pd.to_datetime(missoes_fora_sede_rawdata['Volta'], format='%d/%m/%Y')

missoes_fora_sede_rawdata['Dias fora de sede'] = missoes_fora_sede_rawdata['Volta'] - missoes_fora_sede_rawdata['Ida']
missoes_fora_sede_rawdata['Dias fora de sede'] = missoes_fora_sede_rawdata['Dias fora de sede'].apply(
    lambda x: int(x.days) + 1)

# Mostrando apenas a data
missoes_fora_sede_rawdata['Ida'] = missoes_fora_sede_rawdata['Ida'].apply(lambda x: x.date())
missoes_fora_sede_rawdata['Volta'] = missoes_fora_sede_rawdata['Volta'].apply(lambda x: x.date())

# Carregando todos os trigramas do arquivo Tripulantes
trigramas = pd.Series(map(lambda x: x.trigrama, models.tripulante.tripulantes_list))

# Organizando os dados em wide-data - cada missão é uma coluna
pivot_table = pd.pivot_table(data=missoes_fora_sede_rawdata.reset_index(),
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


# Dados gerais
if st.checkbox('Mostrar dados gerais'):
    col1, col2, col3 = st.columns(3)
    with col1:
        trigramas_selecionados = st.multiselect(label='Trigrama',
                                                options=missoes_fora_sede_rawdata['Trigrama'].unique())
    with col2:
        missoes_selecionadas = st.multiselect(label='Missão',
                                              options=missoes_fora_sede_rawdata['Missão'].unique())
    with col3:
        status_selecionados = st.multiselect(label='Status',
                                             options=missoes_fora_sede_rawdata['Status'].unique())

    # Se não filtrar nada é considerado que todos valores serão mostrados
    if len(trigramas_selecionados) == 0:
        trigramas_selecionados = list(missoes_fora_sede_rawdata['Trigrama'].unique())
    if len(missoes_selecionadas) == 0:
        missoes_selecionadas = list(missoes_fora_sede_rawdata['Missão'].unique())
    if len(status_selecionados) == 0:
        status_selecionados = list(missoes_fora_sede_rawdata['Status'].unique())
    # Aplicando filtros
    st.dataframe(missoes_fora_sede_rawdata.query("Trigrama == @trigramas_selecionados & "
                                                 "Missão == @missoes_selecionadas &"
                                                 "Status == @status_selecionados"), use_container_width=True)

if st.checkbox('Mostrar dados por missão'):
    st.dataframe(pivot_table, use_container_width=True)


# Gráficos
st.markdown('#### Amazônia :deciduous_tree:')
grafico_amazonia = gerar_grafico_missoes_fora_de_sede(data=pivot_table, missao='OPERAÇÃO YANOMAMI/AMAZÔNIA')
st.altair_chart(grafico_amazonia, use_container_width=True)

st.markdown('#### Missões COMPREP')
comprep_table = missoes_fora_sede_rawdata.loc[(missoes_fora_sede_rawdata['Missão'] == 'TÍNIA') |
                                              (missoes_fora_sede_rawdata['Missão'] == 'TÁPIO') |
                                              (missoes_fora_sede_rawdata['Missão'] == 'IVR')]
base_comprep = alt.Chart(comprep_table)
chart_comprep = base_comprep.mark_bar(opacity=0.9).encode(
    x=alt.X('Trigrama:N', sort='-y', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Dias fora de sede):Q'),
    color=alt.Color('Status',
                    scale=alt.Scale(
                        domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                        range=['#70c1ff', '#cccccc', '#8aeba6']
                    )
                    ),
    order=alt.Order('Status', sort='ascending')
)

st.altair_chart(chart_comprep, use_container_width=True)

st.markdown('#### Simulador :video_game:')
grafico_simulador = gerar_grafico_missoes_fora_de_sede(data=pivot_table, missao='SIMULADOR')
st.altair_chart(grafico_simulador, use_container_width=True)

# Gráfico total de dias fora de sede
base_chart = alt.Chart(missoes_fora_sede_rawdata)
chart = base_chart.mark_bar(opacity=0.9).encode(
    x=alt.X('Trigrama:N', sort='-y', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('sum(Dias fora de sede):Q'),
    color=alt.Color('Status',
                    scale=alt.Scale(
                        domain=['CONCLUÍDO', 'PLANEJADO', 'EM ANDAMENTO'],
                        range=['#70c1ff', '#cccccc', '#8aeba6']
                    )),
    order=alt.Order('Status', sort='ascending')
)

st.markdown('#### Total de dias fora de sede :baggage_claim:')
st.altair_chart(chart, use_container_width=True)
