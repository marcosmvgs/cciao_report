import re
import pandas as pd
import streamlit as st


class PilotsDb:
    def __init__(self, raw_database):
        self.raw_database = raw_database
        self.db_flight_registers = self.generate_flight_register_db()

    def generate_flight_register_db(self):

        submission_dates = []
        submission_ids = []
        aircraft_register_numbers = []
        flight_register_types = []

        takeoff_airfields = []
        takeoff_dates = []

        landing_airfields = []
        landing_dates = []

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

        for i, row in self.raw_database.iterrows():
            submission_date = row['Submission Date']
            matricula_anv = row['Matrícula da aeronave']
            tipo_reg = row['Tipo de Registro']
            crew = row['Dados dos Tripulantes'].split('\n')[0:-1]
            dados_dep = row['Dados - Decolagem']
            dados_pouso = row['Dados - Pouso']
            tev = row['Tempo total de voo']
            tev_ifr = row['Tempo IFR']
            tev_not = row['Tempo Noturno']
            descidas = row['Descidas']
            arr_ar = row['Arremetidas no Ar']
            traf_vis = row['Tráfegos Visuais']
            flaps_22 = row['Flaps 22']
            ifr_sem_ap = row['IFR sem AP']
            abt_voo_motivo = row['Motivo da abortiva em Voo']
            abt_solo_motivo = row['Motivo da abortiva no solo']
            submission_id = row['Submission ID']
            obs = row['Observações']
            edit_link = row['Edit Link']

            for crew_member in crew:
                dados_trip_pattern = re.compile(r'Posição:\s*([a-zA-Z0-9]{2,3})\s*,\s*Trigrama:\s*([a-zA-Z]{3})\s*,'
                                                r'\s*Função:\s*(AL|IN|OP),\s*Código OI:\s*([a-zA-Z0-9]{5,7})\s*')
                match_obj_dados_trip = re.search(dados_trip_pattern, crew_member)
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
                    r'(Origem|Destino):\s*([a-zA-Z]{4})\s*,\s*Data\s*-\s*(DEP|Pouso):'
                    r'\s*([0-9]{1,2}-[0-9]{1,2}-[0-9]{4})'
                    r'\s*,\s*Hora\(Z\)\s*-\s*(DEP|Pouso):\s*([0-9]{2}:[0-9]{2})'
                )
                match_obj_dep = re.search(dep_pouso_pattern, dados_dep)
                trash_group0, dep_loc, trash_group1, dep_date, trash_group2, dep_hora = match_obj_dep.groups()
                del trash_group0, trash_group1, trash_group2

                match_obj_pouso = re.search(dep_pouso_pattern, dados_pouso)
                trash_group0, pouso_loc, trash_group1, pouso_date, trash_group2, pouso_hora = match_obj_pouso.groups()
                del trash_group0, trash_group1, trash_group2

                submission_dates.append(submission_date)
                submission_ids.append(submission_id)
                aircraft_register_numbers.append(matricula_anv)
                posicao_list.append(posicao)
                trigrama_list.append(trigrama)
                funcao_list.append(funcao)
                oi_list.append(oi)
                tev_list.append(tev)
                tev_ifr_list.append(tev_ifr)
                tev_not_list.append(str(tev_not))
                traf_vis_list.append(traf_vis)
                flaps_22_list.append(int(flaps_22))
                ifr_sem_ap_list.append(int(ifr_sem_ap))
                desc_loc_list.append(desc_loc)
                desc_tipo_list.append(desc_tipo)
                desc_proc_list.append(desc_proc)
                desc_qtd_list.append(desc_qtd)
                takeoff_dates.append(pd.to_datetime(f'{dep_date} {dep_hora}', format='%d-%m-%Y %H:%M'))
                takeoff_airfields.append(dep_loc)
                landing_airfields.append(pouso_loc)
                flight_register_types.append(tipo_reg)
                landing_dates.append(pd.to_datetime(f'{pouso_date} {pouso_hora}', format='%d-%m-%Y %H:%M'))
                arr_ar_list.append(int(arr_ar))
                abt_voo_motivo_list.append(abt_voo_motivo)
                abt_solo_motivo_list.append(abt_solo_motivo)
                obs_list.append(obs)
                edit_link_list.append(edit_link)

        pilots_database = pd.DataFrame({'Flight ID': submission_ids,
                                        'Submission Date': submission_dates,
                                        'Matrícula da aeronave': aircraft_register_numbers,
                                        'Tipo de Registro': flight_register_types,
                                        'Origem': takeoff_airfields,
                                        'Data/Hora - DEP': takeoff_dates,
                                        'Destino': landing_airfields,
                                        'Data/Hora - Pouso': landing_dates,
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
