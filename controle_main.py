import datetime
import streamlit as st
import constants
import funcs
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id
from models.squadron_db import SquadronDb
from models.pilots_db import PilotsDb
from models.dashboard_controle import DashboardControle


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane')

connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

raw_flight_register = connection.get_sheet('Registro de Voo')
# Dados de voos individuais
flight_registers = PilotsDb(raw_flight_register)
db_flight_registers = flight_registers.db_flight_registers

# Dados gerais do esquadrão
squadron = SquadronDb(raw_flight_register)
db_squadron = squadron.db_esquadron
squadron_chart = squadron.generate_squadron_chart()
kpi_values = squadron.kpi_values
kpi_values_formatted = squadron.kpi_formated_values

# Dados dashboard
dashboard = DashboardControle(data=db_flight_registers)
current_quarter = 1 + (datetime.date.today().month - 1) // 3
minimum_procedures_table = dashboard.generate_minimum_procedures_table(quarter=current_quarter)
maximum_noflight_days_chart = dashboard.generate_no_flight_time_days_chart()
total_flight_hours_chart = dashboard.generate_pilots_total_flight_hours_chart()

# Dados Sidebar
link_to_form = '[Adicionar Registro de Voo](https://form.jotform.com/231508987327062)'

# EXIBIÇÃO DE DADOS
# KPIS ESQUADRÃO
st.markdown("### Quadro geral de horas de voo :hourglass:")
col1, col2, col3, col4 = st.columns(4)
with col1:
    kpi_horas_totais = st.metric(label='Horas totais', value=funcs.format_time(constants.HORAS_TOTAIS))
    kpi_horas_totais_E99 = st.metric(label='Horas totais E99', value=funcs.format_time(constants.HORAS_TOTAIS_E99))
    kpi_horas_totais_R99 = st.metric(label='Horas totais R99', value=funcs.format_time(constants.HORAS_TOTAIS_R99))
with col2:
    kpi_horas_voadas = st.metric(label='Horas voadas', value=kpi_values_formatted['horas voadas'])
    kpi_horas_voadas_E99 = st.metric(label='Horas voadas_E99', value=kpi_values_formatted['horas voadas E99'])
    kpi_horas_voadas_R99 = st.metric(label='Horas voadas_R99', value=kpi_values_formatted['horas voadas R99'])
with col3:
    kpi_horas_disponiveis = st.metric(label='Horas disponíveis', value=kpi_values_formatted['horas disp'])
    kpi_horas_disponiveis_E99 = st.metric(label='Horas disponíveis E99', value=kpi_values_formatted['horas disp E99'])
    kpi_horas_disponiveis_R99 = st.metric(label='Horas disponíveis R99', value=kpi_values_formatted['horas disp R99'])
with col4:
    kpi_perc_voado = st.metric(label='Percentual voado', value=f'{kpi_values_formatted["perc voado"]}%')
    kpi_perc_voado_E99 = st.metric(label='Percentual voado E99', value=f'{kpi_values_formatted["perc voado E99"]}%')
    kpi_perc_voado_R99 = st.metric(label='Percentual voado R99', value=f'{kpi_values_formatted["perc voado R99"]}%')

# HORAS DE VOO POR MÊS - ESQUADRÃO
st.markdown('---')
st.markdown('### Horas de voo por mês :chart:')
st.markdown('')
st.markdown('')
st.altair_chart(squadron_chart, use_container_width=True)
st.markdown('---')

# TABELA DE VOOS
st.markdown('### Tabela de voos :airplane:')
st.markdown('Cada linha representa o voo de um único tripulante.')
st.markdown('Exemplo: um voo com 8 tripulantes será representado em 8 linhas. Esses voos serão'
            'representados pelo mesmo **Flight ID** ')

mostrar_voos = st.checkbox('Mostrar voos')
if mostrar_voos:
    selected_trigrams = st.multiselect(label='Trigrama', options=db_flight_registers['Trigrama'].unique())
    if not selected_trigrams:
        st.dataframe(db_flight_registers)
    else:
        db_flight_registers_filtered_by_trigram = db_flight_registers.query("Trigrama == @selected_trigrams")
        st.dataframe(db_flight_registers_filtered_by_trigram)

# DASHBOARD
st.markdown(f"#### Adaptação Pilotos", unsafe_allow_html=True)
st.altair_chart(maximum_noflight_days_chart, use_container_width=True)

st.markdown(f"#### Pau de Sebo - Pilotos")
st.altair_chart(total_flight_hours_chart, use_container_width=True)

st.markdown(f'#### Cesta Básica - {current_quarter}º Trimestre')
st.dataframe(minimum_procedures_table)

# SIDEBAR
st.sidebar.markdown(f'{link_to_form} :pencil2:', unsafe_allow_html=True)
st.sidebar.write(f'Última atualização: **{db_flight_registers["Data/Hora - DEP"].max().strftime("%d/%m/%Y - %H:%M")}**')
