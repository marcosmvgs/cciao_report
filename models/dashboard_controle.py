import datetime
import altair as alt
import constants
import pandas as pd
import math
import numpy as np
import funcs
from models.tripulante import tripulantes_list
import streamlit as st


class DashboardControle:


    def __init__(self, data):
        self.data = data
        self.tripulantes = tripulantes_list
        self.pilots = list(map(lambda x: x.ispilot, tripulantes_list))

    def generate_minimum_procedures_table(self, quarter):
        quarter = 3
        # Filtrando os pilotos para cesta básica
        temp_df = self.data[((self.data['Posição'] == 'LSP') |
                             ((self.data['Posição'] == 'RSP') &
                              (self.data['Função'] == 'IN'))) &
                            (self.data['Data/Hora - Pouso'].dt.quarter.isin([quarter]))
                            ]

        # Adicionando coluna de Procedimentos de precisão
        temp_df['Precisão'] = temp_df['Descida - Tipo'].apply(lambda x: self.count_tipo_proc(x)['PR'])
        temp_df['Não Precisão'] = temp_df['Descida - Tipo'].apply(lambda x: self.count_tipo_proc(x)['NP'])
        temp_df['Noturno'] = temp_df['Tempo Noturno'].apply(lambda x: 1 if x != '0:00' else 0)
        temp_df = temp_df.drop(['Descida - Tipo', 'Tempo Noturno'], axis=1)

        minimum_procedures = temp_df.groupby('Trigrama').aggregate({'Flaps 22': 'sum',
                                                                    'Arremetida no Ar': 'sum',
                                                                    'IFR sem AP': 'sum',
                                                                    'Noturno': 'sum',
                                                                    'Precisão': 'sum',
                                                                    'Não Precisão': 'sum'}).reset_index()

        minimum_procedures_db = self.fill_empty_values(data=minimum_procedures,
                                                       fill_value=0)
        minimum_procedures_db.set_index('Trigrama', inplace=True)
        minimum_procedures_db_colored = minimum_procedures_db.style.applymap(self.stylize_minimum_procedures_table,
                                                                             subset=['Flaps 22',
                                                                                     'Arremetida no Ar',
                                                                                     'IFR sem AP',
                                                                                     'Noturno']).applymap(
            self.stylize_minimum_procedures_pr_or_np,
            subset=['Precisão',
                    'Não Precisão'])

        return minimum_procedures_db_colored

    def generate_pilots_total_flight_hours_chart(self):
        pau_sebo = self.data[
            (self.data['Posição'] == 'LSP') | (self.data['Posição'] == 'RSP')].filter(
            items=['Trigrama', 'Tempo total de voo', 'Posição']
        )

        pau_sebo['Horas totais'] = pau_sebo['Tempo total de voo'].apply(
            lambda x: funcs.transform_formated_time_to_minutes(x))
        pau_sebo = pau_sebo.groupby(['Trigrama', 'Posição']).aggregate({'Horas totais': 'sum'})
        pau_sebo_agrupado = pau_sebo.pivot_table(values='Horas totais', index='Trigrama',
                                                 columns='Posição').reset_index()
        pau_sebo_agrupado = pau_sebo_agrupado.fillna(0)
        pau_sebo_agrupado['Horas totais'] = pau_sebo_agrupado['LSP'] + pau_sebo_agrupado['RSP']
        pau_sebo_agrupado['Horas Totais'] = pau_sebo_agrupado['Horas totais'].apply(lambda x: funcs.format_time(x))
        pau_sebo_agrupado['Meta'] = 130
        pau_sebo_agrupado['LSP:'] = pau_sebo_agrupado['LSP'].apply(lambda x: funcs.format_time(x))
        pau_sebo_agrupado['RSP:'] = pau_sebo_agrupado['RSP'].apply(lambda x: funcs.format_time(x))

        pau_sebo_agrupado = self.fill_empty_values(data=pau_sebo_agrupado,
                                                   fill_value={
                                                       'Trigrama': '',
                                                       'LSP': 0,
                                                       'RSP': 0,
                                                       'Horas totais': 0,
                                                       'Horas Totais': '00:00',
                                                       'Meta': 130,
                                                       'LSP:': '00:00',
                                                       'RSP:': '00:00'
                                                   })
        pau_sebo_chart_base = alt.Chart(pau_sebo_agrupado)
        pau_sebo_chart1 = pau_sebo_chart_base.mark_bar(opacity=0.8).encode(
            x=alt.X('Trigrama:N', sort=alt.EncodingSortField(field='Horas totais', order='descending', op='sum'),
                    axis=alt.Axis(labelAngle=0, labelFontSize=16, title='')),
            y=alt.Y('Horas totais:Q', axis=alt.Axis(title='', labelFontSize=16)),
            tooltip=['RSP', 'LSP'])

        pau_sebo_chart2 = pau_sebo_chart1.mark_bar(color='red', opacity=0.8).encode(
            y='LSP:Q')

        pau_sebo_chart3 = pau_sebo_chart2.mark_bar(opacity=0.15,
                                                   color='grey').encode(y='Meta:Q')

        pau_sebo_chart4 = pau_sebo_chart1.mark_text(fontSize=16,
                                                    dy=-10,
                                                    color='grey').encode(
            text='Horas Totais',
        )

        return pau_sebo_chart3 + pau_sebo_chart1 + pau_sebo_chart2 + pau_sebo_chart4

    def generate_officers_total_flight_hours_chart(self):
        pass

    def generate_no_flight_time_days_chart(self):

        adaptacao_database = self.data[(self.data['Posição'] == 'LSP') |
                                       (self.data['Posição'] == 'RSP')].filter(items=['Trigrama',
                                                                                      'Data/Hora - Pouso']). \
            groupby('Trigrama').aggregate({'Data/Hora - Pouso': 'max'}).reset_index()

        fake_date = pd.to_datetime(datetime.datetime.today() - datetime.timedelta(days=100))
        adaptacao_database = self.fill_empty_values(data=adaptacao_database,
                                                    fill_value=fake_date)

        # Calculando quantos dias sem voar
        adaptacao_database['Hoje'] = pd.to_datetime(datetime.date.today())
        adaptacao_database['Dias sem voar'] = (
                (adaptacao_database['Hoje'] - adaptacao_database['Data/Hora - Pouso']) / np.timedelta64(1,
                                                                                                        'D')).apply(
            lambda x: math.ceil(x))
        adaptacao_database = adaptacao_database.drop(['Hoje'], axis=1)

        # Formatando data do último voo para o tooltips hover
        adaptacao_database['Último voo'] = adaptacao_database['Data/Hora - Pouso'].apply(
            lambda x: x.strftime("%d/%m/%Y"))
        adaptacao_database = adaptacao_database.reset_index()

        # Inserindo a qualificação Opeacional, max de dias e limite de data sem voar, de acordo com o arquivo constants.
        adaptacao_database['Qualificação Operacional'] = adaptacao_database['Trigrama'].apply(
            lambda x: constants.qualificacao_opr[x])
        adaptacao_database['Max dias'] = adaptacao_database['Qualificação Operacional'].apply(
            lambda x: constants.max_adaptacao[x])
        adaptacao_database['Limite'] = (
                adaptacao_database['Data/Hora - Pouso'] + adaptacao_database['Max dias'].apply(
            lambda x: pd.Timedelta(days=x))).apply(lambda x: x.strftime('%d/%m/%Y'))
        adaptacao_database['Criterio para barras'] = adaptacao_database.apply(lambda x: self.organize_bars(x), axis=1)

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

        return chart1 + chart2

    def generate_alocated_flight_hours(self):
        pass

    @staticmethod
    def count_tipo_proc(value: str):
        preciosion_procedure = value.replace(',', '').strip().split(' ').count('PR')
        not_precision_procedure = value.replace(',', '').strip().split(' ').count('NP')
        return {'PR': preciosion_procedure,
                'NP': not_precision_procedure}

    @staticmethod
    def stylize_minimum_procedures_table(val):
        if val > 0:
            color = 'rgba(0, 255, 0, 0.2)'
            text_color = 'rgba(0, 149, 16, 1)'
        else:
            color = 'rgba(255, 0, 0, 0.25)'
            text_color = 'rgba(255, 0, 0, 1)'
        return f'background-color: {color}; color: {text_color}; font-weight: bold'

    @staticmethod
    def stylize_minimum_procedures_pr_or_np(val):
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

    @staticmethod
    def organize_bars(row):
        if row['Qualificação Operacional'] == 'AL':
            return row['Dias sem voar'] + 365
        elif row['Qualificação Operacional'] == 'OP':
            return row['Dias sem voar'] + (2 * 365 + 1)
        else:
            return row['Dias sem voar'] + (3 * 365 + 1)

    @staticmethod
    def fill_empty_values(data, fill_value):

        data = data.to_dict(orient='list')
        trigrams = list(map(lambda x: x.trigrama, tripulantes_list))

        for trigram in trigrams:
            if not trigram in data['Trigrama']:
                data['Trigrama'].append(trigram)
            else:
                pass

        max_lengh = len(data['Trigrama'])
        if isinstance(fill_value, dict):
            for key in data:
                if len(data[key]) < max_lengh:
                    data[key] += [fill_value[key]] * (max_lengh - len(data[key]))
        else:
            for key in data:
                if len(data[key]) < max_lengh:
                    data[key] += [fill_value] * (max_lengh - len(data[key]))

        new_data = pd.DataFrame(data)

        return new_data
