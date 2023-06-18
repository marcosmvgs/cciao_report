import pandas as pd
import streamlit as st
import re
from pandas.api.types import (is_datetime64_dtype, is_integer_dtype)
import datetime
import constants
import numpy as np
import math
import altair as alt


@st.cache_data
def load_data():
    sheet_id = '1VO7IlI6DntRmN8MPGUObcCY3lV4N4THfD0MgaNr_8kU'
    df = pd.read_excel(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx', engine='openpyxl')
    df['Submission ID'] = df['Submission ID'].astype(str)
    return df


@st.cache_data
def generate_pilots_data(raw_database):
    mid_database = raw_database.filter(items=['Dados dos Tripulantes',
                                              'Tempo total de voo',
                                              'Tempo IFR',
                                              'Tempo Noturno',
                                              'Tráfegos Visuais',
                                              'Flaps 22',
                                              'IFR sem AP',
                                              'Descidas',
                                              'Dados - Decolagem',
                                              'Dados - Pouso',
                                              'Submission ID',
                                              'Matrícula da aeronave',
                                              'Tipo de Registro',
                                              'Esforço Aéreo',
                                              'Arremetidas no Ar',
                                              'Motivo da abortiva em Voo',
                                              'Motivo da abortiva no solo',
                                              'Observações',
                                              'Numero de Pousos',
                                              'Submission Date',
                                              'Edit Link'])

    submission_date_list = []
    submission_id_list = []
    matricula_anv_list = []
    tipo_reg_list = []

    dep_loc_list = []
    dep_date_list = []

    pouso_loc_list = []
    pouso_date_list = []

    posicao_list = []
    trigrama_list = []
    funcao_list = []
    oi_list = []
    tev_list = []
    tev_ifr_list = []
    tev_not_list = []
    traf_vis_list = []
    flaps_22_list = []
    ifr_sem_ap_list = []
    desc_loc_list = []
    desc_tipo_list = []
    desc_proc_list = []
    desc_qtd_list = []
    arr_ar_list = []
    abt_voo_motivo_list = []
    abt_solo_motivo_list = []
    obs_list = []
    edit_link_list = []

    for i, row in mid_database.iterrows():
        trips = row[0].split('\n')[0:-1]
        tev = row[1]
        tev_ifr = row[2]
        tev_not = row[3]
        traf_vis = row[4]
        flaps_22 = row[5]
        ifr_sem_ap = row[6]
        descidas = row[7]
        dados_dep = row[8]
        dados_pouso = row[9]
        submission_date = row[18]
        submission_id = row[10]
        matricula_anv = row[11]
        tipo_reg = row[12]
        arr_ar = row[14]
        abt_voo_motivo = row[15]
        abt_solo_motivo = row[16]
        obs = row[17]
        edit_link = row[19]

        for trip in trips:
            dados_trip_pattern = re.compile(r'Posição:\s*([a-zA-Z0-9]{2,3})\s*,\s*Trigrama:\s*([a-zA-Z]{3})\s*,'
                                            r'\s*Função:\s*(AL|IN|OP),\s*Código OI:\s*([a-zA-Z0-9]{5,7})\s*')
            match_obj_dados_trip = re.search(dados_trip_pattern, trip)
            posicao, trigrama, funcao, oi = match_obj_dados_trip.groups()
            trigrama = trigrama.upper()
            oi = oi.upper()

            desc_pattern = re.compile(
                r'Localidade:\s*([a-zA-Z]{4})\s*,\s*Quantidade:\s*([0-9]*)\s*,\s*Tipo:\s*([a-zA-Z]{2})'
                r'\s*,\s*Procedimento:\s*([a-zA-Z]*)')
            match_obj_desc = re.findall(desc_pattern, descidas)
            desc_loc = ''
            desc_qtd = 0
            desc_tipo = ''
            desc_proc = ''
            for descida in match_obj_desc:
                desc_loc += f'{descida[0]}, '
                desc_parcial = int(descida[1])
                desc_qtd += desc_parcial
                desc_tipo += f'{descida[2]}, ' * desc_parcial
                desc_proc += f'{descida[3]}, '
            desc_loc = desc_loc[0:-2]
            desc_tipo = desc_tipo[0:-2]
            desc_proc = desc_proc[0:-2]

            dep_pouso_pattern = re.compile(
                r'(Origem|Destino):\s*([a-zA-Z]{4})\s*,\s*Data\s*-\s*(DEP|Pouso):\s*([0-9]{1,2}-[0-9]{1,2}-[0-9]{4})'
                r'\s*,\s*Hora\(Z\)\s*-\s*(DEP|Pouso):\s*([0-9]{2}:[0-9]{2})'
            )
            match_obj_dep = re.search(dep_pouso_pattern, dados_dep)
            trash_group0, dep_loc, trash_group1, dep_date, trash_group2, dep_hora = match_obj_dep.groups()
            del trash_group0, trash_group1, trash_group2

            match_obj_pouso = re.search(dep_pouso_pattern, dados_pouso)
            trash_group0, pouso_loc, trash_group1, pouso_date, trash_group2, pouso_hora = match_obj_pouso.groups()
            del trash_group0, trash_group1, trash_group2

            submission_date_list.append(submission_date)
            submission_id_list.append(submission_id)
            matricula_anv_list.append(matricula_anv)
            posicao_list.append(posicao)
            trigrama_list.append(trigrama)
            funcao_list.append(funcao)
            oi_list.append(oi)
            tev_list.append(tev)
            tev_ifr_list.append(tev_ifr)
            tev_not_list.append(tev_not)
            traf_vis_list.append(traf_vis)
            flaps_22_list.append(flaps_22)
            ifr_sem_ap_list.append(ifr_sem_ap)
            desc_loc_list.append(desc_loc)
            desc_tipo_list.append(desc_tipo)
            desc_proc_list.append(desc_proc)
            desc_qtd_list.append(desc_qtd)
            dep_date_list.append(pd.to_datetime(f'{dep_date} {dep_hora}', format='%d-%m-%Y %H:%M'))
            dep_loc_list.append(dep_loc)
            pouso_loc_list.append(pouso_loc)
            tipo_reg_list.append(tipo_reg)
            pouso_date_list.append(pd.to_datetime(f'{pouso_date} {pouso_hora}', format='%d-%m-%Y %H:%M'))
            arr_ar_list.append(arr_ar)
            abt_voo_motivo_list.append(abt_voo_motivo)
            abt_solo_motivo_list.append(abt_solo_motivo)
            obs_list.append(obs)
            edit_link_list.append(edit_link)

    pilots_database = pd.DataFrame({'Flight ID': submission_id_list,
                                    'Submission Date': submission_date_list,
                                    'Matrícula da aeronave': matricula_anv_list,
                                    'Tipo de Registro': tipo_reg_list,
                                    'Origem': dep_loc_list,
                                    'Data/Hora - DEP': dep_date_list,
                                    'Destino': pouso_loc_list,
                                    'Data/Hora - Pouso': pouso_date_list,
                                    'Posição': posicao_list,
                                    'Trigrama': trigrama_list,
                                    'Função': funcao_list,
                                    'Código OI': oi_list,
                                    'Tempo total de voo': tev_list,
                                    'Tempo IFR': tev_ifr_list,
                                    'Tempo Noturno': tev_not_list,
                                    'Tráfegos Visuais': traf_vis_list,
                                    'Flaps 22': flaps_22_list,
                                    'IFR sem AP': ifr_sem_ap_list,
                                    'Arremetida no Ar': arr_ar_list,
                                    'Descida - Quantidade': desc_qtd_list,
                                    'Descida - Localidade': desc_loc_list,
                                    'Descida - Tipo': desc_tipo_list,
                                    'Descida - Procedimento': desc_proc_list,
                                    'Motivo abortiva em voo': abt_voo_motivo_list,
                                    'Motivo abortiva no solo': abt_solo_motivo_list,
                                    'Observações': obs_list,
                                    'Edit Link': edit_link_list})
    return pilots_database


def filter_dataframe(df: pd.DataFrame):
    # modify = st.sidebar.checkbox('Filtrar dados.')
    # if not modify:
    #     return df
    # df = df.copy()
    modification_container = st.container()
    with modification_container:
        to_filter_columns = st.multiselect('Escolha as colunas que deseja filtrar', df.columns)
    for column in to_filter_columns:
        if is_datetime64_dtype(df[column]):
            user_date_input = st.date_input(f'Ddatas para {column}',
                                                    value=(df[column].min(),
                                                           df[column].max()
                                                           ))
            if len(user_date_input) == 2:
                user_date_input = tuple(map(pd.to_datetime, user_date_input))
                start_date, end_date = user_date_input
                df = df[df[column].between(start_date, end_date)]
        elif is_integer_dtype(df[column]):
            st.write('acha que é inteiro')
            user_number_input = st.slider(f'Número {column}',
                                                  min_value=0,
                                                  max_value=20,
                                                  value=[int(df[column].min()), int(df[column].max())])
            if user_number_input:
                number_min, number_max = user_number_input
                df = df[df[column].between(number_min, number_max)]
        else:
            user_text_input = st.text_input('Procurar por...')
            if user_text_input:
                df = df[df[column].astype(str).str.contains(user_text_input)]
    return df


def count_tipo_proc(value: str):
    pr = value.replace(',', '').strip().split(' ').count('PR')
    np = value.replace(',', '').strip().split(' ').count('NP')
    return {'PR': pr,
            'NP': np}


def colorir_cesta_basica_esquadrao(val):
    if val > 0:
        color = 'rgba(0, 255, 0, 0.2)'
        text_color = 'rgba(0, 149, 16, 1)'
    else:
        color = 'rgba(255, 0, 0, 0.25)'
        text_color = 'rgba(255, 0, 0, 1)'
    return f'background-color: {color}; color: {text_color}; font-weight: bold'


def colorir_cesta_basica_comprep(val):
    if val >= 3:
        background_color = 'rgba(0, 266, 0, 0.2)'
        text_color = 'rgba(0, 149, 16, 1)'
    elif val >= 2:
        background_color = 'rgba(255, 255, 0, 0.4)'
        text_color = 'black'
    else:
        background_color = 'rgba(255, 0, 0, 0.25)'
        text_color = 'rgba(255, 0, 0, 1)'
    return f'background-color: {background_color}; color: {text_color}; font-weight: bold'


def generate_cesta_basica_table(data):
    # Filtrando os pilotos para cesta básica
    temp_df = data[(data['Posição'] == 'LSP') |
                   ((data['Posição'] == 'RSP') &
                    (data['Função'] == 'IN')) &
                   (data['Data/Hora - Pouso'].dt.quarter.isin([1 + (datetime.date.today().month - 1) // 3]))
                   ].filter(items=['Trigrama',
                                   'Flaps 22',
                                   'Arremetida no Ar',
                                   'IFR sem AP',
                                   'Descida - Tipo',
                                   'Tempo Noturno'])

    # Adicionando coluna de Procedimentos de precisão
    temp_df['Precisão'] = temp_df['Descida - Tipo'].apply(lambda x: count_tipo_proc(x)['PR'])
    temp_df['Não Precisão'] = temp_df['Descida - Tipo'].apply(lambda x: count_tipo_proc(x)['NP'])
    temp_df['Noturno'] = temp_df['Tempo Noturno'].apply(lambda x: 1 if x != datetime.time(0, 0, 0) else 0)
    temp_df = temp_df.drop(['Descida - Tipo', 'Tempo Noturno'], axis=1)


    cesta_basica_df = temp_df.groupby('Trigrama').aggregate({'Flaps 22': 'sum',
                                                             'Arremetida no Ar': 'sum',
                                                             'IFR sem AP': 'sum',
                                                             'Noturno': 'sum',
                                                             'Precisão': 'sum',
                                                             'Não Precisão': 'sum'})

    tabela = st.dataframe(cesta_basica_df.style.applymap(colorir_cesta_basica_esquadrao, subset=['Flaps 22',
                                                                                                 'Arremetida no Ar',
                                                                                                 'IFR sem AP',
                                                                                                 'Noturno']).applymap(
        colorir_cesta_basica_comprep,
        subset=['Precisão',
                'Não Precisão']))
    return tabela


def generate_pilots_adapt_table(pilots_database):
    # Criando DataFrame para gerar gráfico de adaptação
    # Filtrando dados
    adaptacao_database = pilots_database[(pilots_database['Posição'] == 'LSP') |
                                         (pilots_database['Posição'] == 'RSP')].filter(items=['Trigrama',
                                                                                              'Data/Hora - Pouso']). \
        groupby('Trigrama').aggregate({'Data/Hora - Pouso': 'max'})

    # Calculando quantos dias sem voar
    adaptacao_database['Hoje'] = pd.to_datetime(datetime.date.today())
    adaptacao_database['Dias sem voar'] = (
            (adaptacao_database['Hoje'] - adaptacao_database['Data/Hora - Pouso']) / np.timedelta64(1, 'D')).apply(
        lambda x: math.ceil(x))
    adaptacao_database = adaptacao_database.drop(['Hoje'], axis=1)

    # Formatando data do último voo para o tooltips hover
    adaptacao_database['Último voo'] = adaptacao_database['Data/Hora - Pouso'].apply(lambda x: x.strftime("%d/%m/%Y"))
    adaptacao_database = adaptacao_database.reset_index()

    # Inserindo a qualificação Opeacional, max de dias e limite de data sem voar, de acordo com o arquivo constants.
    adaptacao_database['Qualificação Operacional'] = adaptacao_database['Trigrama'].apply(
        lambda x: constants.qualificacao_opr[x])
    adaptacao_database['Max dias'] = adaptacao_database['Qualificação Operacional'].apply(
        lambda x: constants.max_adaptacao[x])
    adaptacao_database['Limite'] = (adaptacao_database['Data/Hora - Pouso'] + adaptacao_database['Max dias'].apply(
        lambda x: pd.Timedelta(days=x))).apply(lambda x: x.strftime('%d/%m/%Y'))
    adaptacao_database['Criterio para barras'] = adaptacao_database.apply(lambda x: organizar_barras(x), axis=1)

    chart_base = alt.Chart(adaptacao_database)

    chart1 = chart_base.mark_bar(opacity=1).encode(
        x=alt.X('Trigrama', sort=alt.SortField(field='Criterio para barras', order='descending'),
                axis=alt.Axis(labelAngle=0, labelFontSize=16, labelColor='grey', title='')),
        y=alt.Y('Dias sem voar', axis=alt.Axis(title='')),
        color=alt.Color('Qualificação Operacional', legend=alt.Legend(orient='top'))
    )

    chart2 = chart1.mark_bar(opacity=0.25).encode(
        y=alt.Y('Max dias'),
        tooltip=['Último voo', 'Limite']
    )

    return adaptacao_database, (chart1 + chart2)


def organizar_barras(row):
    if row['Qualificação Operacional'] == 'AL':
        return row['Dias sem voar'] + 365
    elif row['Qualificação Operacional'] == 'OP':
        return row['Dias sem voar'] + (2 * 365 + 1)
    else:
        return row['Dias sem voar'] + (3 * 365 + 1)


def make_delta(time):
    if not isinstance(time, str):
        string_time = time.strftime("%H:%M:%S")
    else:
        string_time = time
    try:
        h, m, s = string_time.split(':')
        m = int(m) / 60
        s = int(s) / 3600
        h = int(h) + m + s
    except:
        h, m = string_time.split(':')
        m = int(m) / 60
        h = int(h) + m
    return h


def formartar_tempo(hour):
    new_hour = int(hour // 1)
    new_minute = int((hour % 1) * 60)
    if new_minute <= 9:
        hour_formated = f'{new_hour}:0{new_minute}'
    else:
        hour_formated = f'{new_hour}:{new_minute}'

    return hour_formated


def generate_pau_sebo_table(pilots_database):
    pau_sebo = pilots_database[(pilots_database['Posição'] == 'LSP') | (pilots_database['Posição'] == 'RSP')].filter(
        items=['Trigrama', 'Tempo total de voo', 'Posição']
    )

    pau_sebo['Horas totais'] = pau_sebo['Tempo total de voo'].apply(lambda x: make_delta(x))
    pau_sebo = pau_sebo.groupby(['Trigrama', 'Posição']).aggregate({'Horas totais':'sum'})
    pau_sebo_agrupado = pau_sebo.pivot_table(values='Horas totais', index='Trigrama', columns='Posição').reset_index()
    pau_sebo_agrupado = pau_sebo_agrupado.fillna(0)
    pau_sebo_agrupado['Horas totais'] = pau_sebo_agrupado['LSP'] + pau_sebo_agrupado['RSP']
    pau_sebo_agrupado['Horas Totais'] = pau_sebo_agrupado['Horas totais'].apply(lambda x: formartar_tempo(x))
    pau_sebo_agrupado['Meta'] = 130
    pau_sebo_agrupado['LSP:'] = pau_sebo_agrupado['LSP'].apply(lambda x: formartar_tempo(x))
    pau_sebo_agrupado['RSP:'] = pau_sebo_agrupado['RSP'].apply(lambda x: formartar_tempo(x))

    pau_sebo_chart_base = alt.Chart(pau_sebo_agrupado)
    pau_sebo_chart1 = pau_sebo_chart_base.mark_bar(opacity=0.8).encode(
        x=alt.X('Trigrama:N', sort=alt.EncodingSortField(field='Horas totais', order='descending', op='sum'),
                axis=alt.Axis(labelAngle=0, labelFontSize=16, title='')),
        y=alt.Y('Horas totais:Q', axis=alt.Axis(title='', labelFontSize=16)),
        tooltip=['RSP:', 'LSP:'])

    pau_sebo_chart2 = pau_sebo_chart1.mark_bar(color='red', opacity=0.8).encode(
        y='LSP:Q')

    pau_sebo_chart3 = pau_sebo_chart2.mark_bar(opacity=0.15,
                                               color='grey').encode(y='Meta:Q')

    pau_sebo_chart4 = pau_sebo_chart1.mark_text(fontSize=16,
                                                dy=-10,
                                                color='grey').encode(
        text='Horas Totais',
    )

    st.altair_chart((pau_sebo_chart3 + pau_sebo_chart1 + pau_sebo_chart2 + pau_sebo_chart4),
                    use_container_width=True)
