import altair as alt
import pandas as pd
import streamlit as st
import constants
import funcs
from google_sheets_connection import registro_de_voo
from models import esquadron_db

st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane')

db_registro_voo_raw = registro_de_voo.copy()
db_registro_voo = funcs.generate_esquadron_data(db_registro_voo_raw)
squadron = esquadron_db.EsquadronDb(db_registro_voo_raw)
db_squadron = squadron.db_esquadron

kpi_values = squadron.kpi_values
kpi_values_formated = squadron.kpi_formated_values

st.markdown("### Quadro geral de horas de voo :hourglass:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_horas_totais = st.metric(label='Horas totais', value=funcs.format_time(constants.HORAS_TOTAIS))
    kpi_horas_totais_E99 = st.metric(label='Horas totais_E99', value=funcs.format_time(constants.HORAS_TOTAIS_E99))
    kpi_horas_totais_R99 = st.metric(label='Horas totais_R99', value=funcs.format_time(constants.HORAS_TOTAIS_R99))
with col2:
    kpi_horas_voadas = st.metric(label='Horas voadas', value=kpi_values_formated['horas voadas'])
    kpi_horas_voadas_E99 = st.metric(label='Horas voadas_E99', value=kpi_values_formated['horas voadas E99'])
    kpi_horas_voadas_R99 = st.metric(label='Horas voadas_R99', value=kpi_values_formated['horas voadas R99'])
with col3:
    kpi_horas_disponiveis = st.metric(label='Horas disponíveis', value=kpi_values_formated['horas disp'])
    kpi_horas_disponiveis_E99 = st.metric(label='Horas disponíveis_E99', value=kpi_values_formated['horas disp E99'])
    kpi_horas_disponiveis_R99 = st.metric(label='Horas disponíveis_R99', value=kpi_values_formated['horas disp R99'])
with col4:
    kpi_perc_voado = st.metric(label='Percentual voado', value=f'{kpi_values_formated["perc voado"]}%')
    kpi_perc_voado_E99 = st.metric(label='Percentual voado_E99', value=f'{kpi_values_formated["perc voado E99"]}%')
    kpi_perc_voado_R99 = st.metric(label='Percentual voado_R99', value=f'{kpi_values_formated["perc voado R99"]}%')


db_squadron_groupedby_month = squadron.group_by_month()
esquadron_base_chart = alt.Chart(db_squadron_groupedby_month)

esquadrao_chart1 = esquadron_base_chart.mark_area(line={'color': 'black',
                                                        'opacity': 0.5},
                                                  opacity=0.5,
                                                  point={'color': 'black',
                                                         'size': 90},
                                                  color=alt.Gradient(
                                                      gradient='linear',
                                                      stops=[alt.GradientStop(color='white', offset=0),
                                                             alt.GradientStop(color='darkgrey', offset=1)],
                                                      x1=1,
                                                      x2=1,
                                                      y1=1,
                                                      y2=0)).encode(
    x=alt.X('Data - DEP:T', timeUnit='month', title=''),
    y=alt.Y('sum(Tempo total de voo)', title='Horas no mês'),
    tooltip=['Horas voadas'])

st.altair_chart(esquadrao_chart1, use_container_width=True)

st.markdown('---')

st.markdown('### Tabela de voos :airplane:')
st.markdown('Cada linha representa o voo de um único tripulante.')
st.markdown('Exemplo: um voo com 8 tripulantes será representado em 8 linhas. Esses voos serão'
            'representados pelo mesmo **Flight ID** ')
mostrar_voos = st.checkbox('Mostrar voos selecionados')
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
