
datos = {
            'HEATER-1':{'co2': 1,'usage': 0,'cost':0},
            #posible heater
            'COMP-1':{'co2': 2,'usage': 0,'cost':0},
            'COMP-3':{'co2': 3,'usage': 0,'cost':0},
            'COMP-4':{'co2': 4,'usage': 0,'cost':0},
            'COOLER-1':{'co2': 5,'usage': 0,'cost':0},
            'COOLER-2':{'co2': 6,'usage': 0,'cost':0},
            'COOLER-3':{'co2': 7,'usage': 0,'cost':0},
            'COOLER-5':{'co2': 8,'usage': 0,'cost':0},
            'COOLER-6':{'co2': 9,'usage': 0,'cost':0},
            'COOLER-7':{'co2': 10,'usage': 0,'cost':0},
            'COOLER-4':{'co2': 11,'usage': 0,'cost':0},
            'FLASH-1':{'co2': 12,'usage': 0,'cost':0},
            'FLASH-3':{'co2': 13,'usage': 0,'cost':0},
            'COLUMN1':{
                'condenser':{'co2': 14,'usage': 0,'cost':0},
                'reboiler':{'co2': 15,'usage': 0,'cost':0},
            },
            'COLUMN2':{
                'condenser':{'co2': 16,'usage': 0,'cost':0},
                'reboiler':{'co2': 17,'usage': 0,'cost':0},
            }
        }

co2_total = 0
for key, value in datos.items():
            # Si el valor es un diccionario, suma el costo
            if isinstance(value, dict):
                # Itera sobre los valores del diccionario interno
                for subkey, subvalue in value.items():
                    # Verifica si subvalue es un diccionario antes de acceder a 'cost'
                    if isinstance(subvalue, dict) and 'co2' in subvalue:
                        co2_total += subvalue['co2']
                    if 'co2' in subkey:co2_total += subvalue