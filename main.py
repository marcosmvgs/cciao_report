import datetime
import numpy as np
import pandas as pd
import streamlit as st

import constants
import funcs
from PIL import Image
import os
import math
import altair as alt

st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - Controle CCIAO',
                   page_icon=':airplane')

st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True
)

st.sidebar.markdown("<h1 style='text-align: center; color: black;'>2°/6° GAV</h1>", unsafe_allow_html=True)
image = Image.open(os.path.normpath(os.path.abspath('2gav6.jpg')))
st.sidebar.image(image, width=120)

# Carregando tabelas
raw_database = funcs.load_data()
pilots_database = funcs.generate_pilots_data(raw_database)
df_filtered = funcs.filter_dataframe(pilots_database)
mostrar_voos = st.checkbox('Mostrar voos selecionados')
if mostrar_voos:
    st.write(df_filtered)

col1, col2 = st.columns(2)
with col1:
    quarter = 1 + (datetime.date.today().month - 1) // 3
    st.markdown(f"<h4 style='text-align: center; color: black;'>Cesta básica - {quarter}º "
                f"trimestre</h1>", unsafe_allow_html=True)
    funcs.generate_cesta_basica_table(pilots_database)
with col2:
    st.markdown(f"<h4 style='text-align: center; color: black;'>Adaptação Pilotos</h1>", unsafe_allow_html=True)

    adaptacao_database, alt_chart = funcs.generate_pilots_adapt_table(pilots_database)

    st.altair_chart(alt_chart, use_container_width=True)

link_to_form = '[Adicionar Registro de Voo](https://form.jotform.com/231508987327062)'
st.sidebar.markdown(link_to_form, unsafe_allow_html=True)
st.sidebar.write(f'Última atualização: {pilots_database["Data/Hora - Pouso"].max().strftime("%d/%m/%Y - %H:%M")}')
