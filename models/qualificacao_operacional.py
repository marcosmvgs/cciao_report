
class QualificacaoOperacional:
    def __init__(self,
                 function,
                 max_noflight_days):

        self.function = function
        self.max_noflight_days = max_noflight_days



class Piloto(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)

class ChefeControlador(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)


class CoordenadorTatico(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)

class MecanicoDeVoo(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)


class MecanicoDeSensores(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)


class Coam(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)


class Oe1(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)

class Oe3(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)

class PilotoEexd(QualificacaoOperacional):
    def __init__(self, function, max_noflight_days):
        super().__init__(function, max_noflight_days)






