class Voo:
    def __init__(self,
                 ident = '',
                 origem = '',
                 destino = '',
                 data_hora_dep = '',
                 data_hora_pouso = '',
                 tempo_voo = '',
                 tempo_noturno = '',
                 tempo_ifr = '',
                 esforco_aereo = '',
                 descidas = '',
                 qtd_pousos = '',
                 trafegos = '',
                 abortiva_solo = '',
                 abortiva_voo = '',
                 tripulantes_no_voo = ''):

        self.ident = ident
        self.origem = origem
        self.destino = destino
        self.data_hora_dep = data_hora_dep
        self.data_hora_pouso = data_hora_pouso
        self.tempo_voo = tempo_voo
        self.tempo_noturno = tempo_noturno
        self.tempo_ifr = tempo_ifr
        self.esforco_aereo = esforco_aereo
        self.descidas = descidas
        self.qtd_pousos = qtd_pousos
        self.trafegos = trafegos
        self.abortiva_solo = abortiva_solo
        self.abortiva_voo = abortiva_voo
        self.tripulantes_no_voo = tripulantes_no_voo


class ListaVoos:
    def __init__(self):
        self._voos = []

    def get_voos(self):
        return self._voos

    def add_voo(self, voo):
        self._voos.append(voo)

    def remove_voo(self, voo):
        self._voos.remove(voo)

