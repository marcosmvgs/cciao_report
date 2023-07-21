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


def trocar_nome_por_trigrama(posto_nome):
    lista_tripulantes = militar.tripulantes_list
    first = next(filter(lambda x: x.nome_guerra in posto_nome, lista_tripulantes), None)
    if first is None:
        return None
    else:
        return first.trigrama
