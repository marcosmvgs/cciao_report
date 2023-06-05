import streamlit as st
import funcs


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - Controle CCIAO',
                   page_icon=':airplane')

st.markdown("<h1 style='text-align: center; color: black;'>2°/6° GAV</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>Registro de Voos - CCIAO</h3>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: black;'>Os dados aqui apresentados estão passíveis de erros, "
            "a fonte oficial é o SAGEM.</h3>", unsafe_allow_html=True)
st.markdown('Para adicionar um registro clique aqui')

# Carregando tabelas
raw_database = funcs.load_data()
pilots_database = funcs.generate_pilots_data(raw_database)
df_filtered = funcs.filter_dataframe(pilots_database)
st.write(df_filtered)
