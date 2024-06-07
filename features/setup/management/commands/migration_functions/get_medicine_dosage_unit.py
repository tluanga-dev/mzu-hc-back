
from features.item.models import MedicineDosageUnit

class DosageUnits:
    tablet = 'tablet'
    capsule = 'capsule'
    ml = 'ml'
    tube = 'tube'
    respules = 'respules'
    vial = 'vial'
    ampoule = 'ampoule'
    mg = 'mg'
    mcg = 'mcg'
    gm = 'gm'
    l = 'l'
    IU = 'IU'
    drop = 'drop'
    spray = 'spray'
    patch = 'patch'
    suppository = 'suppository'
    puff = 'puff'
    inhaler = 'inhaler'
    mEq = 'mEq'
    oz = 'oz'
    tsp = 'tsp'
    strip = 'strip'
    bottle = 'bottle'
    sachet = 'sachet'
    troche = 'troche'
    lozenge = 'lozenge'
    cream = 'cream'
    ointment = 'ointment'
    gel = 'gel'
    solution = 'solution'
    suspension = 'suspension'
    syrup = 'syrup'
    elixir = 'elixir'
    infusion = 'infusion'
    concentrate = 'concentrate'
    granule = 'granule'
    pellet = 'pellet'

dosage_units = DosageUnits()

# strips_tablet
# strips_capsule
# bottle_ml
# tube_mg
# packet_resules
# box_vial
# packet_vial
# packet_ampoule
# box_ampoule
# box_piece

def get_medicine_dosage_unit(label):
 
    if label == 'strip_tablet':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='tablet')
        medicine_dosage_unit_1 = MedicineDosageUnit.objects.get(name='mg')
        return [medicine_dosage_unit,medicine_dosage_unit_1]
    if label == 'strip_capsule':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name=DosageUnits.capsule)
        return [medicine_dosage_unit]
    if label == 'bottle_ml':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='ml')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.bottle)
        return [medicine_dosage_unit,medicine_dosage_unit_2]
       
    if label == 'tube_mg':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='mg')
        return [medicine_dosage_unit]
    if label == 'packet_resules':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='respules')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.ml)
        return [medicine_dosage_unit,medicine_dosage_unit_2]
        return [medicine_dosage_unit]
    if label == 'box_vial':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='vial')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.ml)
        return [medicine_dosage_unit,medicine_dosage_unit_2]
  
    if label == 'packet_vial':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='vial')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.ml)
        return [medicine_dosage_unit,medicine_dosage_unit_2]
    if label == 'packet_ampoule':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='ampoule')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.ml)
        return [medicine_dosage_unit,medicine_dosage_unit_2]
        
    if label == 'box_ampoule':
        medicine_dosage_unit = MedicineDosageUnit.objects.get(name='ampoule')
        medicine_dosage_unit_2 = MedicineDosageUnit.objects.get(name=dosage_units.ml)
        return [medicine_dosage_unit,medicine_dosage_unit_2]

    # if label == 'box_piece':
    #     medicine_dosage_unit = MedicineDosageUnit.objects.get(name='piece')
    #     return [medicine_dosage_unit]
    
    else:
        return []


