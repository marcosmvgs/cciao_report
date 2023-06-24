import streamlit as st


st.set_page_config(layout='wide',
                   page_title='2º/6º GAV - CCIAO',
                   page_icon=':airplane')

# SIDEBAR
link_to_sobreaviso_form = '[Adicionar Registro de Sobreaviso](https://form.jotform.com/231707529076662)'
st.sidebar.markdown(f':pencil2: {link_to_sobreaviso_form}', unsafe_allow_html=True)

# CORPO DA PÁGINA
st.markdown('### Tabela e Gráfico - Sobreaviso em Anápolis')
