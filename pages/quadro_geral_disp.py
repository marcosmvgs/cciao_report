import re

import numpy as np
import streamlit as st
import pandas as pd
from models.tripulante import tripulantes_list
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id
import datetime


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
    elif x == 'FÉRIAS':
        color = 'rgba(193, 0, 193, 0.8)'
    elif x == 'RECESSO':
        color = 'rgba(201, 121, 16, 1)'
    else:
        color = None
    if color is None:
        return None
    else:
        return f'background-color: {color}'


def pintar_legendas(x):
    color = {'Missão fora de sede': 'rgba(255, 30, 30, 0.42)',
             'Indisp não Particular': 'rgba(255, 189, 30, 0.51)',
             'Indisp Particular': 'rgba(121, 121, 121, 0.42)',
             'Sobreaviso': 'rgba(121, 53, 0, 0.47)'}

    return f'background-color: {color[x]}'

def pintar_equipagens(x):
    return


# Conexão com google sheets
connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

# Tabelas
missoes_fora_sede_table = connection.get_sheet('Dias fora de sede!A:F')
indisponibilidades_table = connection.get_sheet('Indisponibilidades!A:H')
sobreaviso_table = connection.get_sheet('Sobreaviso em sede')
plano_ferias_table = connection.get_sheet('Plano de Férias 2°/6° GAV')
dados_dos_militares = connection.get_sheet('Dados dos militares')

motivos_indisp = indisponibilidades_table['Motivo'].unique()
missoes = missoes_fora_sede_table['Missão'].unique()

trigramas = dados_dos_militares['Trigramas'].to_list()
funcoes = list(dados_dos_militares['Função a bordo 1'].replace('', np.nan).dropna().unique())

st.markdown('## Quadro geral de Indisponibilidades')
st.markdown('Este quadro dá uma visão de geral de quais tripulantes estão disponíveis para missões do SOP em cada uma'
            ' das datas')
st.markdown('Selecione abaixo intervalo de datas que deseja verificar')
st.markdown('**Os dados são puxados de planilhas da CCIAO**')

col1, col2 = st.columns(2)
with col1:
    initial_date_box = st.date_input(label='Início')
with col2:
    timedelta = datetime.timedelta(days=15)
    final_date = datetime.date.today() + timedelta
    final_date_box = st.date_input(label='Final', value=final_date)

# Criando datas a partir da inicial e final
dates = pd.date_range(initial_date_box, final_date_box, freq='D')

df_quadro_geral = pd.DataFrame(columns=trigramas, index=dates, data='')

trigramas_selecionados = st.multiselect(label='Filtrar trigramas', options=trigramas)

funcoes_selecionadas = st.multiselect(label='Funções', options=funcoes)

st.markdown('#### Legenda')

legenda = {'1': ['Missão fora de sede'],
           '2': ['Indisp não Particular'],
           '3': ['Indisp Particular'],
           '4': ['Sobreaviso']}

legenda_table = pd.DataFrame(legenda)
st.dataframe(legenda_table.style.applymap(pintar_legendas))

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

inicio_recesso = None
termino_recesso = None
trigrama = None

for i, row in plano_ferias_table.iterrows():
    trigrama = row[2].strip()

    pattern = re.compile("Início: (?P<inicio>(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-20\d\d), Término: "
                         "(?P<termino>(0[1-9]|[12][0-9]|3[01])-(0[1-9]|1[0-2])-20\d\d), Tipo de afastamento: "
                         "(?P<tipo>(Dispensa como recompensa|Férias restantes|Férias|Desconto em Férias|Parcela de Férias|Outro.))\s*")

    recesso = row[5].strip()


    if recesso == 'NATAL':
        inicio_recesso = '26/12/2023'
        termino_recesso = '29/12/2023'
        inicio_recesso = datetime.datetime.strptime(inicio_recesso, '%d/%m/%Y')
        termino_recesso = datetime.datetime.strptime(termino_recesso, '%d/%m/%Y')
        df_quadro_geral[trigrama].loc[inicio_recesso:termino_recesso] = 'RECESSO'

    elif recesso == 'ANO NOVO':
        inicio_recesso = '02/01/2024'
        termino_recesso = '05/01/2024'
        inicio_recesso = datetime.datetime.strptime(inicio_recesso, '%d/%m/%Y')
        termino_recesso = datetime.datetime.strptime(termino_recesso, '%d/%m/%Y')
        df_quadro_geral[trigrama].loc[inicio_recesso:termino_recesso] = 'RECESSO'

    else:
        inicio_recesso = None
        termino_recesso = None

    if row[3] == 'NÃO':
        inicio_recesso = None
        termino_recesso = None

    else:
        periodos = row[4].strip()
        results = re.finditer(pattern, periodos)

        for result in results:
            inicio_ferias = datetime.datetime.strptime(result.group('inicio'), '%d-%m-%Y')
            termino_ferias = datetime.datetime.strptime(result.group('termino'), '%d-%m-%Y')

            df_quadro_geral[trigrama].loc[inicio_ferias:termino_ferias] = "FÉRIAS"


df_quadro_geral.reset_index(inplace=True, names='Datas')
df_quadro_geral['Datas'] = df_quadro_geral['Datas'].dt.strftime('%d/%b - %a')
df_quadro_geral.set_index('Datas', inplace=True)
lista_datas_selecionadas = df_quadro_geral.index.to_list()
equipagens_table = pd.DataFrame(columns=funcoes,
                                index=lista_datas_selecionadas,
                                data='')
if not trigramas_selecionados:
    pass
else:
    df_quadro_geral = df_quadro_geral[trigramas_selecionados]
if not funcoes_selecionadas:
    pass
else:
    trigramas_com_funcoes_selecionadas = dados_dos_militares.loc[(dados_dos_militares['Função a bordo 1'].isin(funcoes_selecionadas))]['Trigramas'].to_list()
    df_quadro_geral = df_quadro_geral[trigramas_com_funcoes_selecionadas]


df_quadro_geral_eixos_invertidos = df_quadro_geral.swapaxes('index', 'columns')
for i, row in equipagens_table.iterrows():
    trigramas_disponiveis_no_dia = df_quadro_geral_eixos_invertidos[i][df_quadro_geral_eixos_invertidos[i].replace('', np.nan).isnull()].index.to_list()
    contagem_funcoes = dados_dos_militares.loc[dados_dos_militares['Trigramas'].isin(trigramas_disponiveis_no_dia)].value_counts(subset=['Função a bordo 1'])
    for indx, value in contagem_funcoes.items():
        funcao = indx
        qtde = value
        equipagens_table.loc[i][funcao] = value

mostrar_equipagens = st.checkbox(label='Mostrar equipagens')
if mostrar_equipagens:
    equipagens_table_estilizada = equipagens_table.style.applymap(pintar_equipagens)
    st.dataframe(equipagens_table, use_container_width=True)

estilizada = df_quadro_geral_eixos_invertidos.style.applymap(pintar_celulas)

st.dataframe(estilizada, use_container_width=True, height=1000)
