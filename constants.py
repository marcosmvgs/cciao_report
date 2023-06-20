import pandas as pd

aluno = 'AL'
operacional = 'OP'
instrutor = 'IN'

qualificacao_opr = {
    'ADN': operacional,
    'BRA': operacional,
    'FUC': instrutor,
    'ISC': instrutor,
    'MOT': operacional,
    'MRC': 'AL',
    'SBR': instrutor,
    'SOE': aluno,
    'VLD': instrutor,
    'MAX': instrutor
}

max_adaptacao = {
    aluno: 21,
    operacional: 36,
    instrutor: 46
}

HORAS_TOTAIS = 1370
HORAS_TOTAIS_E99 = 920
HORAS_TOTAIS_R99 = 450
