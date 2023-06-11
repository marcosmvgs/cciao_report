import datetime

import numpy as np
import streamlit as st

import constants
import funcs
from PIL import Image
import os


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - Controle CCIAO',
                   page_icon=':airplane')

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("<h1 style='text-align: center; color: black;'>2°/6° GAV - Guardião</h1>", unsafe_allow_html=True)
image = Image.open(os.path.normpath(os.path.abspath('2gav6.jpg')))
st.sidebar.image(image, width=120)

# Carregando tabelas
raw_database = funcs.load_data()
pilots_database = funcs.generate_pilots_data(raw_database)

esquadrao_database = raw_database.filter(items=['Matrícula da aeronave',
                                                'Tipo de Registro',
                                                'Tempo total de voo',
                                                'Esforço Aéreo',
                                                'Consumo Combustível (kg)'])
esquadrao_database['Tempo total de voo'] = esquadrao_database['Tempo total de voo'].apply(lambda x: funcs.make_delta(x))

horas_voadas = esquadrao_database['Tempo total de voo'].sum()
horas_disp = constants.HORAS_TOTAIS - horas_voadas
perc_voado = round((horas_voadas / constants.HORAS_TOTAIS) * 100, 2)
horas_voadas_e99 = esquadrao_database[esquadrao_database['Matrícula da aeronave'].str.contains('00|01|02|03|04|05')]['Tempo total de voo'].sum()
horas_disp_e99 = constants.HORAS_TOTAIS_E99 - horas_voadas_e99
horas_voadas_r99 = esquadrao_database[esquadrao_database['Matrícula da aeronave'].str.contains('50|52')]['Tempo total de voo'].sum()
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
st.markdown('---')

st.markdown('### Tabela de voos :airplane:')
st.markdown('Cada linha representa o voo de um único tripulante.')
st.markdown('Exemplo: um voo com 8 tripulantes será representado em 8 linhas. Esses voos serão'
            'representados pelo mesmo **Flight ID** ')
mostrar_voos = st.checkbox('Mostrar voos selecionados')
if mostrar_voos:
    df_filtered = funcs.filter_dataframe(pilots_database)
    st.write(df_filtered)
st.markdown('---')

st.markdown('### Dashboard :chart_with_upwards_trend:')
st.multiselect(label='Selecione as Posições à bordo que deseja visualizar', options=pilots_database['Posição'].unique())
col1, col2 = st.columns(2)
with col1:
    quarter = 1 + (datetime.date.today().month - 1) // 3
    st.markdown(f"<h4 style='text-align: center; color: black;'>Cesta básica - {quarter}º "
                f"trimestre</h1>", unsafe_allow_html=True)

    funcs.generate_cesta_basica_table(pilots_database)
    st.markdown(f"<h4 style='text-align: center; color: black;'>Pau de Sebo - Pilotos</h4>", unsafe_allow_html=True)
    funcs.generate_pau_sebo_table(pilots_database)

with col2:
    st.markdown(f"<h4 style='text-align: center; color: black;'>Adaptação Pilotos</h1>", unsafe_allow_html=True)

    adaptacao_database, alt_chart = funcs.generate_pilots_adapt_table(pilots_database)

    st.altair_chart(alt_chart, use_container_width=True)

st.sidebar.markdown('---')
link_to_form = '[Adicionar Registro de Voo](https://form.jotform.com/231508987327062)'
st.sidebar.markdown(f':pencil2: {link_to_form}', unsafe_allow_html=True)
st.sidebar.write(f'Última atualização: {pilots_database["Data/Hora - Pouso"].max().strftime("%d/%m/%Y - %H:%M")}')
