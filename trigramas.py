from models.tripulante import Tripulante, tripulantes_list

trigramas = set(map(lambda x: x.trigrama, list(filter(lambda x: x.ispilot, tripulantes_list))))
disps = trigramas - {'HEL', 'MOT', 'BRA'} - {'LAU'} - {'FBR', 'REI'} - {'MAX', 'OTM', 'MRC', 'TAI', 'DAT'} - {'FUC', 'SBR', 'ZER'}
disps = ' / '.join(disps)
print(disps)
trigramas_notpilot = set(map(lambda x: x.trigrama, list(filter(lambda x: not x.ispilot, tripulantes_list))))
print(trigramas_notpilot)