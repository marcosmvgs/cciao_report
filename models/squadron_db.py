import constants
import funcs
import re
import pandas as pd
import altair as alt


class SquadronDb:
    def __init__(self,
                 raw_data):
        self.raw_data = raw_data

        db_esquadron = self.raw_data.filter(items=['Matrícula da aeronave',
                                                   'Tipo de Registro',
                                                   'Tempo total de voo',
                                                   'Esforço Aéreo',
                                                   'Consumo Combustível (kg)',
                                                   'Dados - Decolagem'])

        db_esquadron['Tempo total de voo'] = db_esquadron['Tempo total de voo']. \
            apply(lambda x: funcs.transform_formated_time_to_minutes(x))

        data_pattern = re.compile('[0-9]{2}-[0-9]{2}-[0-9]{4}')
        db_esquadron['Data - DEP'] = db_esquadron['Dados - Decolagem'].apply(
            lambda x: re.findall(data_pattern, x)[0])
        db_esquadron['Data - DEP'] = pd.to_datetime(db_esquadron['Data - DEP'], dayfirst=True)
        db_esquadron = db_esquadron.drop(columns='Dados - Decolagem')

        self.db_esquadron = db_esquadron
        self.kpi_values = self.get_kpi_values()
        self.kpi_formated_values = self.get_kpi_values_formated()

    def get_kpi_values(self):
        horas_voadas = self.db_esquadron['Tempo total de voo'].sum()
        horas_disp = constants.HORAS_TOTAIS - horas_voadas
        perc_voado = round((horas_voadas / constants.HORAS_TOTAIS) * 100, 2)

        horas_voadas_e99 = self.db_esquadron[self.db_esquadron['Matrícula da aeronave'].str.contains(
            '00|01|02|03|04|05')][
            'Tempo total de voo'].sum()
        horas_disp_e99 = constants.HORAS_TOTAIS_E99 - horas_voadas_e99
        horas_voadas_r99 = self.db_esquadron[self.db_esquadron['Matrícula da aeronave'].str.contains('50|52')][
            'Tempo total de voo'].sum()
        horas_disp_r99 = constants.HORAS_TOTAIS_R99 - horas_voadas_r99
        perc_voado_e99 = round((horas_voadas_e99 / constants.HORAS_TOTAIS_E99) * 100, 2)
        perc_voado_r99 = round((horas_voadas_r99 / constants.HORAS_TOTAIS_R99) * 100, 2)

        dict_values = {
            'horas voadas': horas_voadas / 60,
            'horas disp': horas_disp / 60,
            'perc voado': perc_voado,
            'horas voadas E99': horas_voadas_e99 / 60,
            'horas disp E99': horas_disp_e99 / 60,
            'horas voadas R99': horas_voadas_r99 / 60,
            'horas disp R99': horas_disp_r99 / 60,
            'perc voado E99': perc_voado_e99,
            'perc voado R99': perc_voado_r99
        }
        return dict_values

    def get_kpi_values_formated(self):
        dict_formated_values = {
            'horas voadas': funcs.format_time(self.kpi_values['horas voadas'] * 60),
            'horas disp': funcs.format_time(self.kpi_values['horas disp'] * 60),
            'perc voado': self.kpi_values['perc voado'],
            'horas voadas E99': funcs.format_time(self.kpi_values['horas voadas E99'] * 60),
            'horas disp E99': funcs.format_time(self.kpi_values['horas disp E99'] * 60),
            'horas voadas R99': funcs.format_time(self.kpi_values['horas voadas R99'] * 60),
            'horas disp R99': funcs.format_time(self.kpi_values['horas disp R99'] * 60),
            'perc voado E99': self.kpi_values['perc voado E99'],
            'perc voado R99': self.kpi_values['perc voado R99']
        }
        return dict_formated_values

    def group_by_month(self):
        db_esquadron_groupedby_month = self.db_esquadron.groupby(pd.Grouper(key='Data - DEP', freq='M')).aggregate(
            {'Tempo total de voo': 'sum'}).reset_index()
        db_esquadron_groupedby_month['Horas voadas'] = db_esquadron_groupedby_month['Tempo total de voo'].apply(
            lambda x: funcs.format_time(x))
        db_esquadron_groupedby_month['Tempo total de voo'] = db_esquadron_groupedby_month['Tempo total de voo'].apply(
            lambda x: x / 60)

        return db_esquadron_groupedby_month

    def generate_squadron_chart(self):
        base_chart = self.group_by_month()
        squadron_flight_hours_chart = alt.Chart(base_chart).mark_area(
            line={'color': 'black', 'opacity': 0.5}, opacity=0.5,
            point={'color': 'black', 'size': 90},
            color=alt.Gradient(gradient='linear',
                               stops=[alt.GradientStop(color='white',
                                                       offset=0),
                                      alt.GradientStop(color='darkgrey',
                                                       offset=1)],
                               x1=1, x2=1, y1=1, y2=0)).encode(
            x=alt.X('Data - DEP:T', timeUnit='month', title=''),
            y=alt.Y('sum(Tempo total de voo)', title='Horas no mês'),
            tooltip=['Horas voadas'])

        return squadron_flight_hours_chart
