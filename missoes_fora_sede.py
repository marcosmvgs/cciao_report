class Missao:
    def __init__(self,
                 nome,
                 localidade,
                 data_inicio,
                 data_termino,
                 militares_escalados,
                 ):
        self.nome = nome
        self.localidade = localidade
        self.data_inicio = data_inicio,
        self.data_termino = data_termino
        self.militares_escalados = militares_escalados



class MilitarEmMissao:
    def __init__(self,
                 militar,
                 data_ida,
                 data_volta,
                 modalidade_pagamento):
        self.militar = militar
        self.data_ida = data_ida,
        self.data_volta = data_volta,
        self.modalidade_pagamento = modalidade_pagamento
