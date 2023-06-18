import streamlit as st
import tabela_indisponibilidade
import altair as alt


indisp_table = tabela_indisponibilidade.indisp_dataframe
indisp_base_chart = alt.Chart(tabela_indisponibilidade.indisp_grouped)

indisp_chart1 = indisp_base_chart.mark_bar().encode(
    x=alt.X('Tripulante', sort='-y'),
    y=alt.Y('sum(Dias OUT)'))

st.altair_chart(indisp_chart1, use_container_width=True)
