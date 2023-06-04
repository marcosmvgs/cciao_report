import streamlit as st
import funcs


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - Controle CCIAO',
                   page_icon=':airplane')


# Carregando tabelas
raw_database = funcs.load_data()
pilots_database = funcs.generate_pilots_data(raw_database)




