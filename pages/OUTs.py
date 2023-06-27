from datetime import datetime
import pandas as pd
import streamlit as st
import tabela_indisponibilidade
import altair as alt
from functools import reduce

import tripulante

st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO - Outs',
                   page_icon=':airplane')

indisp_table = tabela_indisponibilidade.indisp_dataframe

indisp_mensal_grouped = indisp_table.groupby([pd.Grouper(key='Data', freq='M'),
                                              'Trigrama'])['Trigrama'].value_counts().reset_index()

st.sidebar.markdown('#### Tabela Geral')

# Filtros - sidebar
filtro_trip = st.sidebar.multiselect(label='Trigramas', options=indisp_table['Trigrama'].unique())

col1, col2 = st.sidebar.columns(2)
with col1:
    filtro_data_inicio = st.date_input(label='Início')
with col2:
    filtro_data_termino = st.date_input(label='Término')

filtro_dias_out = st.sidebar.slider(label='Dias OUT', value=100)
filtro_motivo = st.sidebar.multiselect(label='Motivo', options=indisp_table['Motivo'].unique())
filtro_motivo_obs = st.sidebar.multiselect(label='Observação', options=indisp_table['Motivo - OBS'].unique())

st.markdown('### Tabela e Gráfico de indisponibilidade - Geral')
st.markdown('Clique no botão abaixo para mostrar os dados. Se necessário, filtre os dados na coluna à esquerda.')



# Gráfico
chart_base_indisp_geral = alt.Chart(indisp_table)
chart1_indisp_geral = chart_base_indisp_geral.mark_bar(opacity=0.8).encode(
    y=alt.X('Trigrama:N', sort='-x', axis=alt.Axis(labelLimit=200)),
    x='count(Trigrama):Q')

col1_geral, col2_geral = st.columns(2)
with col1_geral:
    st.dataframe(indisp_table, use_container_width=True)
with col2_geral:
    st.altair_chart(chart1_indisp_geral, use_container_width=True)

st.markdown('### Tabela e Gráfico Indisponibilidade Mensal')

if st.checkbox(label='Mostrar dados', key='tabela_mensal'):
    st.dataframe(indisp_mensal_grouped, use_container_width=True)

# Filtro tripulante
filtro_trip_mes = st.multiselect(label='Selecione os tripulantes', options=indisp_table['Trigrama'].unique())

# Gráfico INDISP mensal
chart_base_indisp_mensal = alt.Chart(indisp_mensal_grouped)

charts = []
if len(filtro_trip_mes) > 0:
    qtd_militares = len(filtro_trip_mes)
    for militar in filtro_trip_mes:
        chart_base_militar = alt.Chart(indisp_mensal_grouped[indisp_mensal_grouped['Trigrama'] == militar])
        chart = chart_base_militar.mark_area(opacity=0.3,
                                             interpolate='cardinal').encode(
            x=alt.X('month(Data):T', title=''),
            y=alt.Y('sum(count):Q', title='Dias OUT'),
            color='Trigrama:N')
        charts.append(chart)

    st.altair_chart((reduce(lambda x, y: x + y, charts)), use_container_width=True)
else:
    chart_indisp_mensal = chart_base_indisp_mensal.mark_area(opacity=0.5,
                                                             interpolate='cardinal').encode(
        x=alt.X('month(Data):T', title=''),
        y=alt.Y('count(Trigrama):Q', title='Militares OUT no mês'),
    )
    st.altair_chart(chart_indisp_mensal, use_container_width=True)

# Verificação de disponibilidade
st.markdown('### Checar disponibilidade de militares - SAGEM :hammer:')

col_data1, col_data2 = st.columns(2)
with col_data1:
    data_inicial = st.date_input(label='Data inicial', value=datetime.today())
    st.markdown('#### Militares indisponíveis')

with col_data2:
    data_final = st.date_input(label='Data final', value=datetime.today())
    st.markdown('#### Militares disponíveis')

col1_tabela_indisp, col2_tabela_disp = st.columns(2)
with col1_tabela_indisp:
    militares_indisponiveis_table = indisp_table.loc[(indisp_table['Data'] >= pd.to_datetime(data_inicial)) &
                                                     (indisp_table['Data'] <= pd.to_datetime(data_final))]. \
        reset_index().drop(columns=['index'])
    militares_indisponiveis = set(militares_indisponiveis_table['Trigrama'].unique())
    st.dataframe(militares_indisponiveis_table, use_container_width=True)

with col2_tabela_disp:
    st.markdown('Todos')
    lista_trigramas = set(map(lambda x: x.trigrama, tripulante.tripulantes_list))
    militares_disponiveis = lista_trigramas - militares_indisponiveis
    texto_militares_disponiveis = ' / '.join(militares_disponiveis)
    st.write(texto_militares_disponiveis)
    st.markdown('Instrutores')
    st.markdown('Operacionais')
    st.markdown('Alunos')
