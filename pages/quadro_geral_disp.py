import streamlit as st
import pandas as pd
from models.tripulante import tripulantes_list
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id

st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane',
                   initial_sidebar_state='collapsed')


def pintar_celulas(x):
    if x in motivos_indisp:
        if x == 'PARTICULAR':
            color = 'rgba(121, 121, 121, 0.42)'
        elif x == 'MARYBA':
            color = 'rgba(0, 130, 127, 0.3)'
        else:
            color = 'rgba(255, 189, 30, 0.51)'
    elif x in missoes:
        color = 'rgba(255, 30, 30, 0.42)'
    elif x == 'SOBREAVISO':
        color = 'rgba(121, 53, 0, 0.47)'
    else:
        color = None
    if color is None:
        return None
    else:
        return f'background-color: {color}'


connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

missoes_fora_sede_table = connection.get_sheet('Dias fora de sede!A:F')
indisponibilidades_table = connection.get_sheet('Indisponibilidades!A:H')
sobreaviso_table = connection.get_sheet('Sobreaviso em sede')

motivos_indisp = indisponibilidades_table['Motivo'].unique()
missoes = missoes_fora_sede_table['Missão'].unique()

st.markdown('## Quadro geral de Indisponibilidades')
st.markdown('Este quadro dá uma visão de geral de quais tripulantes estão disponíveis para missões do SOP em cada uma'
            ' das datas')
st.markdown('Selecione abaixo o intervalo de datas que deseja verificar')
st.markdown('**Os dados são puxados de planilhas da CCIAO**')

col1, col2 = st.columns(2)
with col1:
    initial_date = st.date_input(label='Início')
with col2:
    final_date = st.date_input(label='Final', value=pd.to_datetime('2023-09-02'))

st.markdown('#### Legenda')


def pintar_legendas(x):
    color = {'Missão fora de sede': 'rgba(255, 30, 30, 0.42)',
             'Indisp não Particular': 'rgba(255, 189, 30, 0.51)',
             'Indisp Particular': 'rgba(121, 121, 121, 0.42)',
             'Sobreaviso': 'rgba(121, 53, 0, 0.47)'}

    return f'background-color: {color[x]}'


legenda = {'1': ['Missão fora de sede'],
           '2': ['Indisp não Particular'],
           '3': ['Indisp Particular'],
           '4': ['Sobreaviso']}

legenda_table = pd.DataFrame(legenda)
st.dataframe(legenda_table.style.applymap(pintar_legendas))


dates = pd.date_range(initial_date, final_date, freq='D')
trigramas = list(map(lambda x: x.trigrama, tripulantes_list))
df_quadro_geral = pd.DataFrame(columns=trigramas, index=dates, data='')

estilizada = None
for i, row in missoes_fora_sede_table.iterrows():
    trigrama = row[0].strip()
    missao = row[1].strip()
    ida = row[2].strip()
    volta = row[3].strip()
    status = row[4].strip()

    df_quadro_geral[trigrama].loc[pd.to_datetime(ida, format="%d/%m/%Y"):
                                  pd.to_datetime(volta, format="%d/%m/%Y")] = missao

for i, row in indisponibilidades_table.iterrows():
    trigrama = row[0].strip()
    motivo = row[1].strip()
    inicio = row[3].strip()
    final = row[4].strip()

    df_quadro_geral[trigrama].loc[pd.to_datetime(inicio, format="%d/%m/%Y"):
                                  pd.to_datetime(final, format="%d/%m/%Y")] = motivo

for i, row in sobreaviso_table.iterrows():
    trigrama = row[0].strip()
    inicio_sobreaviso = row[2].strip()
    termino_sobreaviso = row[3].strip()

    df_quadro_geral[trigrama].loc[pd.to_datetime(inicio_sobreaviso, format="%d/%m/%Y"):
                                  pd.to_datetime(termino_sobreaviso, format="%d/%m/%Y")] = 'SOBREAVISO'

df_quadro_geral.reset_index(inplace=True, names='Datas')
df_quadro_geral['Datas'] = df_quadro_geral['Datas'].dt.strftime('%d/%b - %a')
df_quadro_geral.set_index('Datas', inplace=True)
estilizada = df_quadro_geral.swapaxes('index', 'columns').style.applymap(pintar_celulas)

st.dataframe(estilizada, use_container_width=True, height=1000)
