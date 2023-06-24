import pandas as pd
import funcs

df = pd.read_excel('Missões fora de sede.xlsx')

df['Trigrama'] = df['Militar'].apply(funcs.trocar_nome_por_trigrama)
df = df.drop(columns=['Militar'])
df = df[['Trigrama', 'Missão', 'Ida', 'Volta', 'Verificado']]

df = df[df['Trigrama'].str.strip().astype(bool)]
df.to_excel('Controle_dias_fora_de_sede.xlsx')
