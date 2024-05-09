from CodeLibrary import Simulation


def get_HeatDuty(sim):
        """
        Funcion que captura el co2 y el uso de la sustancia en utilities 
        """
        blocks = sim.ListBlocks()
        costos = {
             
        }
        datos = {
            'HEATER-1':{'co2': 0,'usage': 0,'cost':0
            },
            #posible heater
            'COMP-1':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COMP-3':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COMP-4':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-1':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-2':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-3':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-5':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-6':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-7':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COOLER-4':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'FLASH-1':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'FLASH-3':{
                'co2': 0,
                'usage': 0,
                'cost':0
            },
            'COLUMN1':{
                'condenser':{
                    'co2': 0,
                    'usage': 0,
                    'cost':0},
                'reboiler':{
                    'co2': 0,
                    'usage': 0,
                    'cost':0},
            },
            'COLUMN2':{
                'condenser':{
                    'co2': 0,
                    'usage': 0,
                    'cost':0},
                'reboiler':{
                    'co2': 0,
                    'usage': 0,
                    'cost':0},
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
                print(name)

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
                print(name)


        # Inicializa la suma de costos
        suma_costos = 0.0

        # Itera sobre los elementos del diccionario
        for key, value in datos.items():
            # Si el valor es un diccionario, suma el costo
            if isinstance(value, dict):
                # Itera sobre los valores del diccionario interno
                for subvalue in value.values():
                    # Verifica si subvalue es un diccionario antes de acceder a 'cost'
                    if isinstance(subvalue, dict) and 'cost' in subvalue:
                        suma_costos += subvalue['cost']
                    else:
                        print("El valor no tiene la clave 'cost':", subvalue)
            else:
                # Si el valor no es un diccionario, imprime un mensaje de advertencia
                print("El valor no es un diccionario:", value)

        # Imprime la suma de costos
        print("La suma de los costos es:", suma_costos) 
        
        return suma_costos


sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)
convergence = sim.Run()
sim.DialogSuppression(TrueOrFalse= False)
#utl = sim.AspenSimulation.Tree.FindNode("\\Data\\Blocks\\COLUMN2\\Output\\UTL_PADUTY").Value

print(get_HeatDuty(sim=sim))



datos2 = {
    'HEATER-1': 'LPSTEAM',#########
    #posible heater
    'COMP-1':'EL',#########
    'COMP-3':'EL',#########
    'COMP-4':'EL',#########
    'COOLER-1':'WATER',#########
    'COOLER-2':'WATER',#########
    'COOLER-3':'WATER',#########
    'COOLER-4':'WATER',#########
    'COOLER-5':'WATER',#########
    'COOLER-6':'WATER',#########
    'COOLER-7':'WATER',#########
    'FLASH-1':'WATER',###########
    'FLASH-3':'WATER',###########
    'COLUMN1': 'WATER', #########
    'COLUMN1':'MPSTEAM',#########
    'COLUMN2': 'WATER',##########
    'COLUMN2':'MPSTEAM',#########

}
