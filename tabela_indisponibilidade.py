import datetime

import pandas as pd
import re
from bs4 import BeautifulSoup

import funcs

html_source_sagem_indisp = 'tabela_indisponibilidade.html'

with open(html_source_sagem_indisp, 'r', encoding='utf8') as f:
    contents = f.read()
    soup = BeautifulSoup(contents, 'lxml')
    indisp_table = soup.findAll(id='form1:tableIndisponibilidades_data')[0]
    html_rows = indisp_table.findAll('tr')

    indisp_data = []
    for html_row in html_rows:
        html_row = html_row.findAll('td')
        raw_rows = []
        for raw_row in html_row:
            raw_rows.append(raw_row.get_text())

        indisp_data.append(raw_rows)

indisp_raw_dataframe = pd.DataFrame(indisp_data, columns=['índice', 'Tripulante', 'Motivo'])
indisp_raw_dataframe = indisp_raw_dataframe.filter(items=['Tripulante', 'Motivo'])

tripulante_list = []
inicio_data_hora_list = []
termino_data_hora_list = []
motivo_list = []

for i, row in indisp_raw_dataframe.iterrows():
    tripulante = row[0]
    indisps_text = row[1]

    pattern = re.compile("(\d{1,2}-\s+indisponibilidade (?P<texto_periodo>(?P<indisp_total>de (?P<total_inicio>(0[1-9]|"
                         "[12][0-9]|3[01])\/(0[1-9]|1[12])\/20\d\d (([01][0-9]|2[0-3]):([0-5][0-9]))) a "
                         "(?P<total_termino>(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[12])\/20\d\d (([01][0-9]|2[0-3]):"
                         "([0-5][0-9]))))|(?P<indisp_parcial>entre ((?P<parcial_hora_inicio>([01][0-9]|2[0-3]):"
                         "([0-5][0-9])) e (?P<parcial_hora_termino>([01][0-9]|2[0-3]):([0-5][0-9])) no período de "
                         "(?P<parcial_data_inicio>(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[12])\/20\d\d)) a "
                         "(?P<parcial_data_termino>(0[1-9]|[12][0-9]|3[01])\/(0[1-9]|1[12])\/20\d\d))) "
                         "por motivo de (?P<motivo>([A-zÃÁ-úÀ-ù]\s*)*"
                         "(\.|,|(?P<motivo_obs>\(Obs:\s+([\&\#\?\$\*\%A-zÃÁ-úÀ-ù0-9\/,\.-]\s*)*)\))))")

    results = re.finditer(pattern, indisps_text)
    for result in results:
        motivo = result.group('motivo')
        if result.group('indisp_total') is None:
            parcial_data_inicio = result.group('parcial_data_inicio')
            parcial_hora_inicio = result.group('parcial_hora_inicio')
            parcial_data_hora_inicio = datetime.datetime.strptime(
                f"{parcial_data_inicio}  {parcial_hora_inicio}", '%d/%m/%Y %H:%M')

            parcial_data_termino = result.group('parcial_data_termino')
            parcial_hora_termino = result.group('parcial_hora_termino')
            parcial_data_hora_termino = datetime.datetime.strptime(
                f"{parcial_data_termino}  {parcial_hora_termino}", '%d/%m/%Y %H:%M')

            diff_days = parcial_data_hora_termino - parcial_data_hora_inicio


            for d in range(diff_days.days + 1):
                next_day = parcial_data_hora_inicio + datetime.timedelta(days=d)
                datetime_indisp_inicio = parcial_data_hora_inicio+ \
                                         datetime.timedelta(days=d)
                datetime_indisp_termino = next_day + \
                                          datetime.timedelta(
                                              seconds=(parcial_data_hora_termino.time().hour -
                                                       parcial_data_hora_inicio.time().hour )* 3600)

                tripulante_list.append(tripulante)
                inicio_data_hora_list.append(datetime_indisp_inicio)
                termino_data_hora_list.append(datetime_indisp_termino)
                motivo_list.append(motivo.replace(',', ''))
        else:

            datetime_indisp_inicio = datetime.datetime.strptime(result.group('total_inicio'), "%d/%m/%Y %H:%M")
            datetime_indisp_termino = datetime.datetime.strptime(result.group('total_termino'), "%d/%m/%Y %H:%M")

            tripulante_list.append(tripulante)
            inicio_data_hora_list.append(datetime_indisp_inicio)
            termino_data_hora_list.append(datetime_indisp_termino)
            motivo_list.append(motivo.replace(',', ''))


inicio = pd.to_datetime(pd.Series(inicio_data_hora_list), format='%d/%m/%Y %H:%M')
termino = pd.to_datetime(pd.Series(termino_data_hora_list), format='%d/%m/%Y %H:%M')


def adjusting_days_out(dias):
    days = dias.days

    if dias.seconds >= 12 * 3600:
        days += 1
    else:
        pass
    return days


dias_out = (termino - inicio).apply(lambda x: adjusting_days_out(x))

indisp_dataframe = pd.DataFrame({'Tripulante': tripulante_list,
                                 'Início - data/hora': inicio,
                                 'Término - data/hora': termino,
                                 'Dias OUT': dias_out,
                                 'Motivo': motivo_list})
indisp_dataframe = indisp_dataframe.drop(indisp_dataframe.loc[indisp_dataframe['Dias OUT'] == 0].index)

indisp_grouped = indisp_dataframe.groupby([pd.Grouper(key='Início - data/hora', freq='M'), 'Tripulante']).sum('Dias OUT').reset_index()
