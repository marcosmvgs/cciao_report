import datetime
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id
import pandas as pd
import streamlit as st
from models import esquadrao

st.set_page_config(page_title='Registro de voo',
                   page_icon=':airplane:',
                   layout='wide')

# Conexão com google sheets
connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

# Tabelas
missoes_fora_sede_table = connection.get_sheet('Registro de Voo!A:U')

st.write('### Pesquisar Registro de Voo')
st.write('Aqui eu posso ter um mecanismo de busca de voo - pode ser a própria tabela de voos'
         'com filtros, encontrando um voo eu posso ver o ID e lançar no form pelo ID')
st.dataframe(missoes_fora_sede_table)
st.text_input(label='ID do voo')

col1_alterar, col2_deletar, col3_duplicar, col4_vazia = st.columns([1, 1, 1, 10])

with col1_alterar:
    st.button(label='Alterar')
with col2_deletar:
    st.button(label='Deletar')
with col3_duplicar:
    st.button(label='Duplicar')

st.write('### Registro de voo')

with st.form("my_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        origem = st.text_input(label='Origem', value='SBAN')
        destino = st.text_input(label='Destino')
    with col2:
        dep_date = st.date_input(label='Data - DEP', format='DD/MM/YYYY', key='dep_date')
        pouso_date = st.date_input(label='Data - Pouso', format='DD/MM/YYYY')
    with col3:
        dep_time = st.time_input(label='Hora-Z - DEP', step=300,)
        pouso_time = st.time_input(label='Hora-Z - Pouso')

    col1_anv, col2_tev, col3_tev_ifr, col4_tev_not, col5_pousos, col6_esfaer, col7_abortiva = st.columns(7)
    with col1_anv:
        anv = st.selectbox(label='Aeronave', options=esquadrao.eqsae.aeronaves)
    with col2_tev:
        tev = st.time_input(label='Tempo de Voo', step=300)
    with col3_tev_ifr:
        tev_ifr = st.time_input(label='Tempo IFR real', step=300)
    with col4_tev_not:
        tev_not = st.time_input(label='Tempo noturno', step=300)
    with col5_pousos:
        pousos = st.number_input(label='Qtd Pousos', step=1, min_value=1)
    with col6_esfaer:
        esforco = st.text_input(label='Esforço Aéreo', value='SESQAE')
    with col7_abortiva:
        abortiva = st.selectbox(label='Abortiva', options=['VMAT', 'VMET', 'VOSP', 'VIES', 'VDTI'])

    col1_descidas, col2_tripulantes = st.columns(2)
    with col1_descidas:

        st.write('Descidas')
        descidas_df = pd.DataFrame({'Localidade': [''],
                                    'Quantidade': [''],
                                    'Precisão': [False],
                                    'Procedimento': [''],
                                    'Arremetida no ar': [False],
                                    'Tráfego Visual': [False],
                                    'Flape 22º': [False],
                                    'IFR sem PA': [False]})

        edited_descidas_df = st.data_editor(descidas_df,
                                            num_rows='dynamic')

        st.checkbox(label='Realizou LOFT?')

    with col2_tripulantes:
        st.write('Tripulantes')
        tripulantes_df = pd.DataFrame(
            {'Posição': [''],
             'Trigrama': [''],
             'Ordem de Instr.': [''],
             'Função': ['']}
        )

        edited_tripulantes_df = st.data_editor(tripulantes_df,
                                               num_rows='dynamic',
                                               column_config={
                                                   'Trigrama': st.column_config.SelectboxColumn(
                                                       'Trigrama',
                                                       options=[
                                                           'MRC',
                                                           'DAT',
                                                           'MAX',
                                                           'VLD'
                                                       ]
                                                   )
                                               },
                                               use_container_width=True
                                               )

        st.number_input(label='Consumo de Combustível (kg)', step=1)

    # Every form must have a submit button.
    submitted = st.form_submit_button("Registrar")
    if submitted:
        st.success('Voo registrado com sucesso')

