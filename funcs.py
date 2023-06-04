import pandas as pd
import streamlit as st
import re


def load_data():
    sheet_id = '1RJlJBlPjvRitroGBc7GoutKFXnYJor5rwEN8ax3f6oM'
    df = pd.read_excel(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx')
    df['Submission ID'] = df['Submission ID'].astype(str)
    return df


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
    dep_hora_list = []

    pouso_loc_list = []
    pouso_date_list = []
    pouso_hora_list = []

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
        submission_date = row[19]
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
                desc_qtd += int(descida[1])
                desc_tipo += f'{descida[2]}, '
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
            dep_date_list.append(dep_date)
            dep_loc_list.append(dep_loc)
            pouso_loc_list.append(pouso_loc)
            dep_hora_list.append(dep_hora)
            tipo_reg_list.append(tipo_reg)
            pouso_date_list.append(pouso_date)
            pouso_hora_list.append(pouso_date)
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
                                    'Data - DEP': dep_date_list,
                                    'Hora - DEP': dep_hora_list,
                                    'Destino': pouso_loc_list,
                                    'Data - Pouso': pouso_date_list,
                                    'Hora - Pouso': pouso_hora_list,
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

    st.write(pilots_database)
