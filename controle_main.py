import datetime
import re
import altair as alt
import pandas as pd
import streamlit as st
import constants
import funcs
from google_sheets_connection import registro_de_voo


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane')


registro_voo_raw_database = registro_de_voo
pilots_database = funcs.generate_pilots_data(registro_voo_raw_database)

esquadrao_database = registro_voo_raw_database.filter(items=['Matrícula da aeronave',
                                                             'Tipo de Registro',
                                                             'Tempo total de voo',
                                                             'Esforço Aéreo',
                                                             'Consumo Combustível (kg)',
                                                             'Dados - Decolagem'])

esquadrao_database['Tempo total de voo'] = esquadrao_database['Tempo total de voo'].\
    apply(lambda x: funcs.formarted_time_to_hourstime(x))

data_pattern = re.compile('[0-9]{2}-[0-9]{2}-[0-9]{4}')
esquadrao_database['Data - DEP'] = esquadrao_database['Dados - Decolagem'].apply(
    lambda x: re.findall(data_pattern, x)[0])
esquadrao_database['Data - DEP'] = pd.to_datetime(esquadrao_database['Data - DEP'], dayfirst=True)
esquadrao_database = esquadrao_database.drop(columns='Dados - Decolagem')

horas_voadas = esquadrao_database['Tempo total de voo'].sum()
horas_disp = constants.HORAS_TOTAIS - horas_voadas
perc_voado = round((horas_voadas / constants.HORAS_TOTAIS) * 100, 2)
horas_voadas_e99 = esquadrao_database[esquadrao_database['Matrícula da aeronave'].str.contains('00|01|02|03|04|05')][
    'Tempo total de voo'].sum()
horas_disp_e99 = constants.HORAS_TOTAIS_E99 - horas_voadas_e99
horas_voadas_r99 = esquadrao_database[esquadrao_database['Matrícula da aeronave'].str.contains('50|52')][
    'Tempo total de voo'].sum()
horas_disp_r99 = constants.HORAS_TOTAIS_R99 - horas_voadas_r99
perc_voado_e99 = round((horas_voadas_e99 / constants.HORAS_TOTAIS_E99) * 100, 2)
perc_voado_r99 = round((horas_voadas_r99 / constants.HORAS_TOTAIS_R99) * 100, 2)

st.markdown("### Quadro geral de horas de voo :hourglass:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_horas_totais = st.metric(label='Horas totais', value=funcs.formartar_tempo(constants.HORAS_TOTAIS))
    kpi_horas_totais_E99 = st.metric(label='Horas totais_E99', value=funcs.formartar_tempo(constants.HORAS_TOTAIS_E99))
    kpi_horas_totais_R99 = st.metric(label='Horas totais_R99', value=funcs.formartar_tempo(constants.HORAS_TOTAIS_R99))
with col2:
    kpi_horas_voadas = st.metric(label='Horas voadas', value=funcs.formartar_tempo(horas_voadas))
    kpi_horas_voadas_E99 = st.metric(label='Horas voadas_E99', value=funcs.formartar_tempo(horas_voadas_e99))
    kpi_horas_voadas_R99 = st.metric(label='Horas voadas_R99', value=funcs.formartar_tempo(horas_voadas_r99))
with col3:
    kpi_horas_disponiveis = st.metric(label='Horas disponíveis', value=funcs.formartar_tempo(horas_disp))
    kpi_horas_disponiveis_E99 = st.metric(label='Horas disponíveis_E99', value=funcs.formartar_tempo(horas_disp_e99))
    kpi_horas_disponiveis_R99 = st.metric(label='Horas disponíveis_R99', value=funcs.formartar_tempo(horas_disp_r99))
with col4:
    kpi_perc_voado = st.metric(label='Percentual voado', value=f'{perc_voado}%')
    kpi_perc_voado_E99 = st.metric(label='Percentual voado_E99', value=f'{perc_voado_e99}%')
    kpi_perc_voado_R99 = st.metric(label='Percentual voado_R99', value=f'{perc_voado_r99}%')


esquadrao_database_text = esquadrao_database.groupby(pd.Grouper(key='Data - DEP', freq='M')).aggregate(
    {'Tempo total de voo': 'sum'}).reset_index()
st.write(funcs.formartar_tempo(esquadrao_database['Tempo total de voo'].sum()))
esquadrao_database_text['Horas voadas'] = esquadrao_database_text['Tempo total de voo'].apply(
    lambda x: funcs.formartar_tempo(x))

base_text_chart = alt.Chart(esquadrao_database_text)

esquadrao_chart1 = alt.Chart(esquadrao_database).mark_area(line={'color': 'grey',
                                                                 'opacity': 0.3},
                                                           opacity=0.5,
                                                           point={'color': 'black',
                                                                  'size': 90},
                                                           color=alt.Gradient(
                                                               gradient='linear',
                                                               stops=[alt.GradientStop(color='white', offset=0),
                                                                      alt.GradientStop(color='grey', offset=1)],
                                                               x1=1,
                                                               x2=1,
                                                               y1=1,
                                                               y2=0)).encode(
    x=alt.X('Data - DEP:T', timeUnit='month', title=''),
    y='sum(Tempo total de voo)',
    tooltip=['sum(Tempo total de voo)'])

esquadrao_chart2 = alt.Chart(esquadrao_database).mark_line().encode(
    x=alt.X('Data - DEP:T', timeUnit='month', title=''),
    y=alt.Y('sum(Tempo total de voo)', axis=alt.Axis(title='')),
    color=alt.Color('Matrícula da aeronave:N', legend=alt.Legend(orient='top')),
)

esquadrao_chart3 = base_text_chart.mark_text(fontSize=18,
                                             dy=-15,
                                             color='grey').encode(
    text='Horas voadas:N',
    x=alt.X('Data - DEP:T', timeUnit='month', title=''),
    y='sum(Tempo total de voo)'
)

st.altair_chart((esquadrao_chart1 + esquadrao_chart2 + esquadrao_chart3), use_container_width=True)

st.markdown('---')
#
# st.markdown('### Tabela de voos :airplane:')
# st.markdown('Cada linha representa o voo de um único tripulante.')
# st.markdown('Exemplo: um voo com 8 tripulantes será representado em 8 linhas. Esses voos serão'
#             'representados pelo mesmo **Flight ID** ')
# mostrar_voos = st.checkbox('Mostrar voos selecionados')
# df_filtered = funcs.filter_dataframe(pilots_database)
# if mostrar_voos:
#     st.write(df_filtered)
# st.markdown('---')
#
# st.markdown('### Dashboard :chart_with_upwards_trend:')
# st.multiselect(label='Selecione as Posições à bordo que deseja visualizar', options=pilots_database['Posição'].unique())
# col1, col2 = st.columns(2)
# with col1:
#     quarter = 1 + (datetime.date.today().month - 1) // 3
#     st.markdown(f"<h4 style='text-align: center; color: black;'>Cesta básica - {quarter}º "
#                 f"trimestre</h1>", unsafe_allow_html=True)
#
#     funcs.generate_cesta_basica_table(pilots_database)
#     st.markdown(f"<h4 style='text-align: center; color: black;'>Pau de Sebo - Pilotos</h4>", unsafe_allow_html=True)
#     funcs.generate_pau_sebo_table(pilots_database)
#
# with col2:
#     st.markdown(f"<h4 style='text-align: center; color: black;'>Adaptação Pilotos</h1>", unsafe_allow_html=True)
#
#     adaptacao_database, alt_chart = funcs.generate_pilots_adapt_table(pilots_database)
#
#     st.altair_chart(alt_chart, use_container_width=True)
#
# link_to_form = '[Adicionar Registro de Voo](https://form.jotform.com/231508987327062)'
# st.sidebar.markdown(f'{link_to_form} :pencil2:', unsafe_allow_html=True)
# st.sidebar.write(f'Última atualização: **{pilots_database["Data/Hora - DEP"].max().strftime("%d/%m/%Y - %H:%M")}**')
