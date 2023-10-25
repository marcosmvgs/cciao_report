from models import tripulante


class Esquadrao:
    def __init__(self,
                 aeronaves,
                 tripulantes,):
        self.aeronaves = aeronaves
        self.tripulantes = tripulantes


lista_tripulantes = tripulante.tripulantes_list

eqsae = Esquadrao(aeronaves=[6700, 6701, 6702, 6703, 6704, 6750, 6752],
                  tripulantes=lista_tripulantes)
