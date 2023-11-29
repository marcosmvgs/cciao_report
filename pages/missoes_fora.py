import streamlit as st
import altair as alt
from google_sheets_connection import GoogleSheetsApi, scope, spreadsheet_id


st.set_page_config(page_icon=':airplane:',
                   page_title='Dias fora de sede',
                   layout='wide',
                   initial_sidebar_state='collapsed')

connection = GoogleSheetsApi(scopes=scope,
                             spread_sheet_id=spreadsheet_id)

tabela_dias_fora_sede = connection.get_sheet('Dias fora de sede!A:I').dropna()

# Conteúdo de apresentação da página
st.markdown('### Tabelas e Gráficos de missões fora sede :bar_chart:')
st.markdown('O objetivo dessa página:')
st.markdown(
    ' 1. Ser transparente com todos os militares quanto á quantos dias cada militar está ficando fora de sede.\n'
    '2. Facilitar o serviço da escala no momento de escalar um militar para missões fora de sede. ')
st.markdown(
    'Todos os dados aqui lançados são baseados na planilha de controle de missões fora de sede da CCIAO. '
    'Caso algum militar perceba alguma discrepância, '
    'favor avisar a CCIAO para que possamos ajustar o mais rápido possível e não trabalharmos com dados errados.')

# Filtros
ch_filter = st.multiselect(label='Círculo Hierárquico', options=tabela_dias_fora_sede['Círculo Hierárquico'].unique())
function_filter = st.multiselect(label='Função', options=tabela_dias_fora_sede['Função'].unique())
mission_cat_filter = st.multiselect(label='Categoria da Missão', options=tabela_dias_fora_sede['Categoria da Missão'].unique())
mission_filter = st.multiselect(label='Missão', options=tabela_dias_fora_sede['Missão'].unique())

filtered_table = tabela_dias_fora_sede
if ch_filter:
    filtered_table = filtered_table.query("`Círculo Hierárquico` == @ch_filter")
if function_filter:
    filtered_table = filtered_table.query("`Função` == @function_filter")
if mission_cat_filter:
    filtered_table = filtered_table.query("`Categoria da Missão` == @mission_cat_filter")
if mission_filter:
    filtered_table = filtered_table.query("`Missão` == @mission_filter")

if st.checkbox('Mostrar tabela de dados'):
    st.dataframe(filtered_table, use_container_width=True)

base = alt.Chart(filtered_table)

new_chart = base.mark_bar(color='red',
                          opacity=0.9, ).encode(
    x=alt.X('Trigrama:N', sort='-y', title='', axis=alt.Axis(labelAngle=0)),
    y=alt.Y(f'sum(Dias fora de sede):Q', title='Dias fora de sede'),
    color=alt.Color('Categoria da Missão',
                    scale=alt.Scale(
                    ), legend=alt.Legend(orient='top')),
    order=alt.Order('Status', sort='ascending')
)
st.altair_chart(new_chart, use_container_width=True)
