from CodeLibrary import Simulation


def get_HeatDuty(sim):
        """
        Funcion que captura el co2 y el uso de la sustancia en utilities 
        """
        blocks = sim.ListBlocks()
        costos = {
             
        }
        datos = {
            'HEATER-1':{'co2': 0,'usage': 0,'cost':0},
            #posible heater
            'COMP-1':{'co2': 0,'usage': 0,'cost':0},
            'COMP-3':{'co2': 0,'usage': 0,'cost':0},
            'COMP-4':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-1':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-2':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-3':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-5':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-6':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-7':{'co2': 0,'usage': 0,'cost':0},
            'COOLER-4':{'co2': 0,'usage': 0,'cost':0},
            'FLASH-1':{'co2': 0,'usage': 0,'cost':0},
            'FLASH-3':{'co2': 0,'usage': 0,'cost':0},
            'COLUMN1':{
                'condenser':{'co2': 0,'usage': 0,'cost':0},
                'reboiler':{'co2': 0,'usage': 0,'cost':0},
            },
            'COLUMN2':{
                'condenser':{'co2': 0,'usage': 0,'cost':0},
                'reboiler':{'co2': 0,'usage': 0,'cost':0},
            }
        }
        for name,typ in blocks.items():
            if typ == 'RadFrac':
                condenser_co2rate = sim.BLK_RADFRAC_Get_Condenser_Co2Rate(name) #capturar el co2 del condensador de la columna
                if condenser_co2rate == None: condenser_co2rate = 0 
                condenser_usage = sim.BLK_RADFRAC_Get_Condenser_Usage(name) #capturar el uso de agua para el condensador
                condenser_cost = sim.BLK_RADFRAC_Get_Condenser_Cost(name)# se caputura el costo de operacion del equipo compr
                if condenser_cost==None: condenser_cost = 0
                reboiler_co2rate = sim.BLK_RADFRAC_Get_Reboiler_Co2Rate(name) #capturar el co2 del reboiler de la columna
                if reboiler_co2rate == None : reboiler_co2rate = 0
                reboiler_usege = sim.BLK_RADFRAC_Get_Reboiler_Usage(name) #capturar el uso de MPSTEAM para el reboiler
                reboiler_cost = sim.BLK_RADFRAC_Get_Reboiler_Cost(name) # se caputura el costo de operacion del equipo column reboiler
                if reboiler_cost == None: reboiler_cost = 0
                datos[name]['condenser']['co2'] = condenser_co2rate
                datos[name]['condenser']['usage'] = condenser_usage
                datos[name]['condenser']['cost'] = condenser_cost
                datos[name]['reboiler']['co2'] = reboiler_co2rate
                datos[name]['reboiler']['usage'] = reboiler_usege
                datos[name]['reboiler']['cost'] = reboiler_cost

            elif typ == 'Flash2':
                if name == 'FLASH-2': continue

                flash_co2rate = sim.BLK_FLASH2_Get_utility_co2rate(name)#captura el co2 de los equipos flash
                if flash_co2rate == None: flash_co2rate = 0
                flash_usage = sim.BLK_FLASH2_Get_utility_usage(name)#captura el usage de los equipos flash
                flash_cost = sim.BLK_FLASH2_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if flash_cost == None: flash_cost = 0

                datos[name]['co2'] = flash_co2rate
                datos[name]['usage'] = flash_usage
                datos[name]['cost'] =flash_cost
            elif typ == 'Heater':
                if name == 'HEATER-2': continue

                heater_co2rate = sim.BLK_HEATER_Get_utility_co2rate(name)#captura el co2 de los equipos heater
                if heater_co2rate == None: heater_co2rate = 0
                heater_usage = sim.BLK_HEATER_Get_utility_usage(name)#captura el usage de los equipos heater
                heater_cost = sim.BLK_HEATER_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if heater_cost == None: heater_cost = 0
                datos[name]['co2'] = heater_co2rate
                datos[name]['usage'] = heater_usage
                datos[name]['cost'] = heater_cost

            elif typ == 'Compr':
                compr_co2rate = sim.BLK_COMPR_Get_utility_co2rate(name) # se caputura el co2 del equipo compr
                if compr_co2rate == None: compr_co2rate = 0
                compr_cost = sim.BLK_COMPR_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if compr_cost == None: compr_cost = 0
                compr_usage = sim.BLK_COMPR_Get_utility_usage(name)

                datos[name]['co2'] = compr_co2rate
                datos[name]['usage'] = compr_usage
                datos[name]['cost'] = compr_cost


        # Inicializa la suma de costos
        suma_costos = 0.0
        co2_total = 0
        # Itera sobre los elementos del diccionario
        for key, value in datos.items():
            # Si el valor es un diccionario, suma el costo
            if isinstance(value, dict):
                # Itera sobre los valores del diccionario interno
                for subkey, subvalue in value.items():
                    # Verifica si subvalue es un diccionario antes de acceder a 'cost'
                    if isinstance(subvalue, dict) and 'cost' in subvalue:
                        suma_costos += subvalue['cost']
                    if 'cost' in subkey: suma_costos += subvalue
        
        for key, value in datos.items():
            # Si el valor es un diccionario, suma el costo
            if isinstance(value, dict):
                # Itera sobre los valores del diccionario interno
                for subkey, subvalue in value.items():
                    # Verifica si subvalue es un diccionario antes de acceder a 'cost'
                    if isinstance(subvalue, dict) and 'co2' in subvalue:
                        co2_total += subvalue['co2']
                    if 'co2' in subkey:co2_total += subvalue
                    
        
        return suma_costos, co2_total,datos


sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)
convergence = sim.Run()
sim.DialogSuppression(TrueOrFalse= False)
#utl = sim.AspenSimulation.Tree.FindNode("\\Data\\Blocks\\COLUMN2\\Output\\UTL_PADUTY").Value

print(get_HeatDuty(sim=sim))


{'HEATER-1': {'co2': 0.73029661, 'usage': 5.63144703, 'cost': 0.0489780252},
'COMP-1': {'co2': 355.376176, 'usage': 1138.49773, 'cost': 62.6173749}, 
'COMP-3': {'co2': 18.822681, 'usage': 60.3011144, 'cost': 3.31656129}, 
'COMP-4': {'co2': 29.7935282, 'usage': 95.4477715, 'cost': 5.24962743}, 
'COOLER-1': {'co2': 0, 'usage': 1112263.29, 'cost': 399.695691}, 
'COOLER-2': {'co2': 0, 'usage': 488824.175, 'cost': 175.660672}, 
'COOLER-3': {'co2': 0, 'usage': 12010.2304, 'cost': 4.31591816}, 
'COOLER-5': {'co2': 0, 'usage': 24659.9837, 'cost': 8.86165114}, 
'COOLER-6': {'co2': 0, 'usage': 18483.4423, 'cost': 6.64208946}, 
'COOLER-7': {'co2': 0, 'usage': 37218.2459, 'cost': 13.3745064}, 
'COOLER-4': {'co2': 0, 'usage': 20520.4564, 'cost': 7.37409756}, 
'FLASH-1': {'co2': 0, 'usage': 58.5401921, 'cost': 0.0210366222}, 
'FLASH-3': {'co2': 0, 'usage': 2.89093335e-11, 'cost': 1.03886698e-14}, 
'COLUMN1': {'condenser': {'co2': 0, 'usage': 1623.7829, 'cost': 0.583512049}, 
            'reboiler': {'co2': 82.024966, 'usage': 681.352638, 'cost': 6.06107615}}, 
'COLUMN2': {'condenser': {'co2': 0, 'usage': 438215.695, 'cost': 157.474338}, 
            'reboiler': {'co2': 590.352008, 'usage': 4903.84718, 'cost': 43.6229194}}}