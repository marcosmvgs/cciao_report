from datetime import datetime, timedelta
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
data_indisp_list = []
motivo_list = []
motivo_obs_list = []

for i, row in indisp_raw_dataframe.iterrows():
    tripulante = row[0]
    indisps_text = row[1]

    pattern = re.compile(
        "\d{1,2}-\s+indisponibilidade (?P<texto_periodo>(?P<indisp_total>de (?P<total_inicio>(0[1-9]|[12][0-9]|3[01])/"
        "(0[1-9]|1[0-2])/20\d\d (([01][0-9]|2[0-3]):([0-5][0-9]))) a (?P<total_termino>(0[1-9]|[12][0-9]|3[01])/"
        "(0[1-9]|1[0-2])/20\d\d (([01][0-9]|2[0-3]):([0-5][0-9]))))|(?P<indisp_parcial>entre "
        "((?P<parcial_hora_inicio>([01][0-9]|2[0-3]):([0-5][0-9])) e (?P<parcial_hora_termino>([01][0-9]|2[0-3]):"
        "([0-5][0-9])) no período de (?P<parcial_data_inicio>(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/20\d\d))"
        " a (?P<parcial_data_termino>(0[1-9]|[12][0-9]|3[01])/(0[1-9]|1[0-2])/20\d\d))) por motivo de"
        " (?P<motivo>([A-zÃÁ-úÀ-ù]\s*)*(\.|,|))\s*"
        "((?P<motivo_obs>\(Obs:\s*[0-9:,\.\(&\#\?\$\*\%A-zÃÁ-úÀ-ù0-9\/\s\.-]*\)*)|)")

    results = re.finditer(pattern, indisps_text)
    for result in results:
        # Cada result é um texto de indisponibilidade do militar (match)
        motivo = result.group('motivo')
        motivo_obs = result.group('motivo_obs')

        if result.group('indisp_total'):

            data_inicial = datetime.strptime(result.group('total_inicio'), '%d/%m/%Y %H:%M')
            data_final = datetime.strptime(result.group('total_termino'), '%d/%m/%Y %H:%M')
            days = data_final - data_inicial

            for delta_day in range(days.days + 1):
                data_indisp = data_inicial + timedelta(days=delta_day)

                tripulante_list.append(tripulante)
                data_indisp_list.append(data_indisp)
                motivo_list.append(motivo.replace(',', ''))
                motivo_obs_list.append(motivo_obs)

        else:

            hora_inicial = int(result.group('parcial_hora_inicio').split(':')[0].strip())
            hora_final = int(result.group('parcial_hora_termino').split(':')[0].strip())

            if (hora_final - hora_inicial) >= 4 or (hora_final - hora_inicial) == 0:

                data_inicial = datetime.strptime(result.group('parcial_data_inicio'), '%d/%m/%Y')
                data_final = datetime.strptime(result.group('parcial_data_termino'), '%d/%m/%Y')
                days = data_final - data_inicial

                for delta_day in range(days.days + 1):

                    data_indisp = data_inicial + timedelta(days=delta_day)

                    tripulante_list.append(tripulante)
                    data_indisp_list.append(data_indisp)
                    motivo_list.append(motivo.replace(',', ''))
                    motivo_obs_list.append(motivo_obs)
            else:
                pass

data = pd.to_datetime(pd.Series(data_indisp_list), format='%d/%m/%Y')
indisp_raw_dataframe = pd.DataFrame({'Tripulante': tripulante_list,
                                     'Data': data_indisp_list,
                                     'Motivo': motivo_list,
                                     'Motivo - OBS': motivo_obs_list})

indisp_dataframe = indisp_raw_dataframe[
    (indisp_raw_dataframe['Tripulante'].str.contains('QO')) & (indisp_raw_dataframe['Data'].dt.year == 2023)]


indisp_dataframe['Tripulante'] = indisp_dataframe['Tripulante'].apply(lambda x: funcs.trocar_nome_por_trigrama(x))
indisp_dataframe = indisp_dataframe.rename(columns={'Tripulante': 'Trigrama'})
