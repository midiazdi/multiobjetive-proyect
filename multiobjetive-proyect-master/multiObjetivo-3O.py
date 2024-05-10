import numpy as np
from pymoo.core.problem import Problem
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize
from CodeLibrary import Simulation
from pymoo.core.problem import ElementwiseProblem
from pymoo.core.mutation import Mutation
from pymoo.visualization.scatter import Scatter
import time
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PolynomialMutation
from pymoo.operators.sampling.rnd import FloatRandomSampling
from pymoo.operators.selection.tournament import  TournamentSelection
from pymoo.operators.mutation.pm import PM
from multiprocessing.pool import ThreadPool
from pymoo.core.problem import StarmapParallelization
import multiprocessing
from pymoo.core.population import Population
import pandas as pd





#####################################
#Abrir simulacion
#####################################








class MyOptimizationProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        xl = np.zeros(6)
        xu = np.ones(6)
        super().__init__(n_var=6, n_obj=2, n_constr=2, xl=xl, xu=xu, **kwargs)
        #self.sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)
        self.sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/midia/OneDrive/Escritorio/pablo" ,VISIBILITY=False)
        self.blocks = self.sim.ListBlocks()
        self.penaltis = 400
        self.lower = np.array([10,190,10,0.1,2500,0.1])
        self.upper = np.array([120,300,10000,4.5,75000,0.97])
        self.diff = self.upper - self.lower
        self.execution_count = 0  # Añadir un contador de ejecuciones
        self.max_executions_before_restart = 1500
    def iniciar(self):
        #self.sim.CloseAspen()
        self.sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)

    def _evaluate(self, x, out, *args, **kwargs):
        
        if self.execution_count == self.max_executions_before_restart:
            self.sim.EngineReinit()
            self.execution_count=0
        try:
            convergence, x1 , x2, massFrac_metoh = self.aspen(x)
        except:
            print("Error en _evaluate")
            self.iniciar()
            convergence, x1 , x2, massFrac_metoh = self.aspen(x)
        restr_convergencia = 0 if convergence else 1
        #restr_massFrac_metoh = -1 if massFrac_metoh is not None else 1
        #Restricción de fracción masica de metanol: debe ser >= 0.8, reformula para pymoo
        restr_fraccion_masica = 0.95 - massFrac_metoh if massFrac_metoh is not None else 1
        

        # Asigna las restricciones calculadas al diccionario 'out'
        out["G"] = np.array([restr_convergencia, restr_fraccion_masica])
        out["F"] = np.array([-x1,x2]) 
        self.execution_count += 1
        
    
    def aspen(self, x):
        
        decision_var = self.diff*x + self.lower
        ##Asignacion de variables
        print(decision_var)
        self.sim.BLK_RPLUG_Set_InletProcessflowPressure("R-1",decision_var[0]) #asigna la presion del reactor R-1
        self.sim.BLK_RPLUG_Set_T_SPEC_Constant_Temp("R-1", decision_var[1]) #asigna la temperatura del raactor R-1
        self.sim.BLK_RPLUG_Set_WeightOfCatalystLoaded("R-1",decision_var[2]) #asigna el peso del reactor R-1
        self.sim.BLK_RADFRAC_Set_Refluxratio("COLUMN2", decision_var[3]) #asigna la relacion de reflujo de la columna 2
        self.sim.h2(decision_var[4]) # Asigna un valor de entrada para el total flow rate del H2 (metodo creado)
        self.sim.purge(decision_var[5])
        
        #Ejecucion de la simulacion con los nuevos datos
        convergence = self.sim.Run()
        self.sim.DialogSuppression(TrueOrFalse= False)

        #captura de datos con la nueva simulacion
        cost,co2 = self.get_cost_co2()
        massFlow_metoh = self.sim.AspenSimulation.Tree.FindNode("\\Data\\Streams\\METOH\\Output\\MASSFLOW\\MIXED\\CH3OH").Value
        massFrac_metoh = self.sim.AspenSimulation.Tree.FindNode("\\Data\\Streams\\METOH\\Output\\MASSFRAC\\MIXED\\CH3OH").Value
        
        #Evaluacion de restricciones
        
        x1 = massFlow_metoh * 0.37 
        x2 = co2 / 2500
        
        #print(massFlow_metoh,massFrac_metoh, convergence )
        #print(x)
        #print("->>",decision_var)

        return convergence, x1 , x2, massFrac_metoh 

    def get_cost_co2(self):
        """
        Funcion que captura el co2 y el uso de la sustancia en utilities 
        """
        blocks = self.sim.ListBlocks()

    
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
                condenser_co2rate = self.sim.BLK_RADFRAC_Get_Condenser_Co2Rate(name) #capturar el co2 del condensador de la columna
                if condenser_co2rate == None: condenser_co2rate = 0 
                condenser_usage = self.sim.BLK_RADFRAC_Get_Condenser_Usage(name) #capturar el uso de agua para el condensador
                condenser_cost = self.sim.BLK_RADFRAC_Get_Condenser_Cost(name)# se caputura el costo de operacion del equipo compr
                if condenser_cost==None: condenser_cost = 0
                reboiler_co2rate = self.sim.BLK_RADFRAC_Get_Reboiler_Co2Rate(name) #capturar el co2 del reboiler de la columna
                if reboiler_co2rate == None : reboiler_co2rate = 0
                reboiler_usege = self.sim.BLK_RADFRAC_Get_Reboiler_Usage(name) #capturar el uso de MPSTEAM para el reboiler
                reboiler_cost = self.sim.BLK_RADFRAC_Get_Reboiler_Cost(name) # se caputura el costo de operacion del equipo column reboiler
                if reboiler_cost == None: reboiler_cost = 0
                datos[name]['condenser']['co2'] = condenser_co2rate
                datos[name]['condenser']['usage'] = condenser_usage
                datos[name]['condenser']['cost'] = condenser_cost
                datos[name]['reboiler']['co2'] = reboiler_co2rate
                datos[name]['reboiler']['usage'] = reboiler_usege
                datos[name]['reboiler']['cost'] = reboiler_cost

            elif typ == 'Flash2':
                if name == 'FLASH-2': continue

                flash_co2rate = self.sim.BLK_FLASH2_Get_utility_co2rate(name)#captura el co2 de los equipos flash
                if flash_co2rate == None: flash_co2rate = 0
                flash_usage = self.sim.BLK_FLASH2_Get_utility_usage(name)#captura el usage de los equipos flash
                flash_cost = self.sim.BLK_FLASH2_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if flash_cost == None: flash_cost = 0

                datos[name]['co2'] = flash_co2rate
                datos[name]['usage'] = flash_usage
                datos[name]['cost'] =flash_cost
            elif typ == 'Heater':
                if name == 'HEATER-2': continue

                heater_co2rate = self.sim.BLK_HEATER_Get_utility_co2rate(name)#captura el co2 de los equipos heater
                if heater_co2rate == None: heater_co2rate = 0
                heater_usage = self.sim.BLK_HEATER_Get_utility_usage(name)#captura el usage de los equipos heater
                heater_cost = self.sim.BLK_HEATER_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if heater_cost == None: heater_cost = 0
                datos[name]['co2'] = heater_co2rate
                datos[name]['usage'] = heater_usage
                datos[name]['cost'] = heater_cost

            elif typ == 'Compr':
                compr_co2rate = self.sim.BLK_COMPR_Get_utility_co2rate(name) # se caputura el co2 del equipo compr
                if compr_co2rate == None: compr_co2rate = 0
                compr_cost = self.sim.BLK_COMPR_Get_utility_cost(name)# se caputura el costo de operacion del equipo compr
                if compr_cost == None: compr_cost = 0
                compr_usage = self.sim.BLK_COMPR_Get_utility_usage(name)

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
                    
        
        return suma_costos, co2_total



if __name__=="__main__":

    # initialize the thread pool and create the runner
    """n_proccess = 1
    pool = multiprocessing.Pool(n_proccess)
    runner = StarmapParallelization(pool.starmap)

    my_problem = MyOptimizationProblem(elementwise_runner=runner)"""
    df = pd.read_csv("./resultados.csv")

    df = df.iloc[0:19,1:7]

    pop = Population.new("X",df.values) 
    my_problem = MyOptimizationProblem()
    algorithm = NSGA2(pop_size=20,
                 crossover=SBX(eta=11, prob=0.9),
                 mutation=PM(eta=10),sampling=pop)

    result = minimize(my_problem,
                    algorithm,
                    ('n_gen', 30),
                    seed=301,
                    save_history=True,
                    verbose=True)
    
    #print('Threads:', result.exec_time)
    #pool.close()


    print("Solución óptima encontrada:\nVariables de decisión: ", result.X)
    print("Funciones objetivo: ", result.F)

    plot = Scatter()
    plot.add(result.F, color="red")
    plot.show()



