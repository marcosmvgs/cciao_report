import streamlit as st
import altair as alt
from models import tripulante as militar


def transform_formated_time_to_minutes(time):
    if not isinstance(time, str):
        string_time = time.strftime("%H:%M:%S")
    else:
        string_time = time
    try:
        h, m, s = string_time.split(':')
        m = int(m)
        s = int(s) / 60
        time_in_minutes = int(h) * 60 + m + s
    except:
        h, m = string_time.split(':')
        m = int(m)
        time_in_minutes = int(h) * 60 + m
    return time_in_minutes


def format_time(minute):
    hour = minute / 60
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

    pau_sebo['Horas totais'] = pau_sebo['Tempo total de voo'].apply(lambda x: transform_formated_time_to_minutes(x))
    pau_sebo = pau_sebo.groupby(['Trigrama', 'Posição']).aggregate({'Horas totais': 'sum'})
    pau_sebo_agrupado = pau_sebo.pivot_table(values='Horas totais', index='Trigrama', columns='Posição').reset_index()
    pau_sebo_agrupado = pau_sebo_agrupado.fillna(0)
    pau_sebo_agrupado['Horas totais'] = pau_sebo_agrupado['LSP'] + pau_sebo_agrupado['RSP']
    pau_sebo_agrupado['Horas Totais'] = pau_sebo_agrupado['Horas totais'].apply(lambda x: format_time(x))
    pau_sebo_agrupado['Meta'] = 130
    pau_sebo_agrupado['LSP:'] = pau_sebo_agrupado['LSP'].apply(lambda x: format_time(x))
    pau_sebo_agrupado['RSP:'] = pau_sebo_agrupado['RSP'].apply(lambda x: format_time(x))

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

    st.altair_chart((pau_sebo_chart3 + pau_sebo_chart1 + pau_sebo_chart2 + pau_sebo_chart4),
                    use_container_width=True)


def trocar_nome_por_trigrama(posto_nome):
    lista_tripulantes = militar.tripulantes_list
    first = next(filter(lambda x: x.nome_guerra in posto_nome, lista_tripulantes), None)
    if first is None:
        return None
    else:
        return first.trigrama
