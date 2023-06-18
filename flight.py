class Flight:
    def __init__(self,
                 flight_id,
                 submission_date,
                 matricula_anv,
                 tipo_reg,
                 origem,
                 destino,
                 dep,
                 pouso,
                 posicao,
                 trig,
                 funcao,
                 oi,
                 tev,
                 tempo_ifr,
                 tempo_not,
                 traf_visual,
                 flaps_22,
                 ifr_sem_ap,
                 arr_no_ar,
                 descida,
                 abortiva,
                 obs,
                 edit_link):

        self.edit_link = edit_link
        self.obs = obs
        self.abortiva = abortiva
        self.descida = descida
        self.arr_no_ar = arr_no_ar
        self.ifr_sem_ap = ifr_sem_ap
        self.flaps_22 = flaps_22
        self.traf_visual = traf_visual
        self.tempo_not = tempo_not
        self.tempo_ifr = tempo_ifr
        self.tev = tev
        self.oi = oi
        self.funcao = funcao
        self.trig = trig
        self.posicao = posicao
        self.pouso = pouso
        self.dep = dep
        self.destino = destino
        self.origem = origem
        self.tipo_reg = tipo_reg
        self.matricula_anv = matricula_anv
        self.submission_date = submission_date
        self.flight_id = flight_id
