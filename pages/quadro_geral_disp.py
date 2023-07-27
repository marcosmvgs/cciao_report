import streamlit as st
import pandas as pd
from models.tripulante import tripulantes_list
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane',
                   initial_sidebar_state='collapsed')

st.markdown('## Quadro geral de Indisponibilidades')
st.markdown('Este quadro dá uma visão de geral de quais tripulantes estão disponíveis para missões do SOP em cada uma'
            ' das datas')
st.markdown('Selecione abaixo o intervalo de datas que deseja verificar')
st.markdown('**Os dados são puxados de planilhas da CCIAO**')


def pintar_celulas(x):
    if x in motivos_indisp:
        if x == 'PARTICULAR':
            color = 'rgba(121, 121, 121, 0.42)'
        else:
            color = 'rgba(255, 189, 30, 0.51)'
    elif x in missoes:
        color = 'rgba(255, 30, 30, 0.42)'
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

motivos_indisp = indisponibilidades_table['Motivo'].unique()
missoes = missoes_fora_sede_table['Missão'].unique()

col1, col2 = st.columns(2)
with col1:
    initial_date = st.date_input(label='Início')
with col2:
    final_date = st.date_input(label='Final', value=pd.to_datetime('2023-09-02'))

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

    df_quadro_geral[trigrama].loc[pd.to_datetime(ida, format="%d/%m/%Y"):pd.to_datetime(volta,
                                                                                        format="%d/%m/%Y")] = missao

for i, row in indisponibilidades_table.iterrows():
    trigrama = row[0].strip()
    motivo = row[1].strip()
    obs = row[2].strip()
    inicio = row[3].strip()
    final = row[5].strip()
    tipo = row[7].strip()

    df_quadro_geral[trigrama].loc[pd.to_datetime(inicio, format="%d/%m/%Y"):pd.to_datetime(final,
                                                                                           format="%d/%m/%Y")] = motivo

df_quadro_geral.reset_index(inplace=True, names='Datas')
df_quadro_geral['Datas'] = df_quadro_geral['Datas'].dt.strftime('%d-%b-%y')
df_quadro_geral.set_index('Datas', inplace=True)
estilizada = df_quadro_geral.swapaxes('index', 'columns').style.applymap(pintar_celulas)
st.dataframe(estilizada, use_container_width=True, height=1000)
