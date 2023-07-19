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
    'MRC': aluno,
    'SBR': instrutor,
    'SOE': aluno,
    'VLD': instrutor,
    'MAX': instrutor,
    'DAT': instrutor,
    'TAI': instrutor,
    'RPH': instrutor,
    'LAU': instrutor,
    'HEL': operacional,
    'FBR': operacional,
    'HER': operacional,
    'REI': operacional,
    'OTM': aluno,
    'AND': instrutor,
    'ZER': operacional,
    'DNI': operacional,
    'DNS': instrutor,
    'FAB': instrutor,
    'TAL': instrutor,
    'FCI': aluno,
    'DED': instrutor,
}

max_adaptacao = {
    aluno: 21,
    operacional: 36,
    instrutor: 46
}

HORAS_TOTAIS = 1370 * 60
HORAS_TOTAIS_E99 = 920 * 60
HORAS_TOTAIS_R99 = 450 * 60

qualificacoes_operacionais = {
    ''
}

