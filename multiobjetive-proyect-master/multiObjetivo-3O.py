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





#####################################
#Abrir simulacion
#####################################








class MyOptimizationProblem(ElementwiseProblem):

    def __init__(self, **kwargs):
        xl = np.zeros(6)
        xu = np.ones(6)
        super().__init__(n_var=6, n_obj=2, n_constr=2, xl=xl, xu=xu, **kwargs)
        self.sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)
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
        hD = self.get_HeatDuty()
        massFlow_metoh = self.sim.AspenSimulation.Tree.FindNode("\\Data\\Streams\\METOH\\Output\\MASSFLOW\\MIXED\\CH3OH").Value
        massFrac_metoh = self.sim.AspenSimulation.Tree.FindNode("\\Data\\Streams\\METOH\\Output\\MASSFRAC\\MIXED\\CH3OH").Value

        #Evaluacion de restricciones
        
        x1 = massFlow_metoh
        x2 = hD
        
        #print(massFlow_metoh,massFrac_metoh, convergence )
        #print(x)
        #print("->>",decision_var)

        return convergence, x1 , x2, massFrac_metoh 

    def get_HeatDuty(self):
        """
        Funcion que captura el co2 y el uso de la sustancia en utilities 
        """
        datos = {
            'HEATER-1':{
                'co2': 0,
                'usage': 0
            },
            #posible heater
            'COMP-1':{
                'co2': 0,
                'usage': 0
            },
            'COMP-3':{
                'co2': 0,
                'usage': 0
            },
            'COMP-4':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-1':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-2':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-3':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-5':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-6':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-7':{
                'co2': 0,
                'usage': 0
            },
            'COOLER-4':{
                'co2': 0,
                'usage': 0
            },
            'FLASH-1':{
                'co2': 0,
                'usage': 0
            },
            'FLASH-3':{
                'co2': 0,
                'usage': 0
            },
            'COLUMN1':{
                'condenser':{
                    'co2': 0,
                    'usage': 0},
                'reboiler':{
                    'co2': 0,
                    'usage': 0},
            },
            'COLUMN2':{
                'condenser':{
                    'co2': 0,
                    'usage': 0},
                'reboiler':{
                    'co2': 0,
                    'usage': 0},
            }
        }
        for name,typ in self.blocks.items():
            if typ == 'RadFrac':
                #columna1
                condenser_co2rate = self.sim.BLK_RADFRAC_Get_Reboiler_Duty(name) #capturar el co2 del condensador de la columna
                condenser_usage = self.sim.BLK_RADFRAC_Get_Reboiler_Usage(name) #capturar el uso de agua para el condensador
                reboiler_co2rate = self.sim.BLK_RADFRAC_Get_Reboiler_Co2Rate(name) #capturar el co2 del reboiler de la columna
                reboiler_usege = self.sim.BLK_RADFRAC_Get_Reboiler_Usage(name) #capturar el uso de MPSTEAM para el reboiler
                datos[name]['condenser']['co2'] = condenser_co2rate
                datos[name]['condenser']['usage'] = condenser_usage
                datos[name]['reboiler']['co2'] = reboiler_co2rate
                datos[name]['reboiler']['usage'] = reboiler_usege

            elif typ == 'Flash2':
                flash_co2rate = self.sim.BLK_FLASH2_Get_utility_co2rate(name)#captura el co2 de los equipos flash
                flash_usage = self.sim.BLK_FLASH2_Get_utility_usage(name)#captura el usage de los equipos flash

                datos[name]['co2'] = flash_co2rate
                datos[name]['usage'] = flash_usage
            elif typ == 'Heater':
                heater_co2rate = self.sim.BLK_HEATER_Get_utility_co2rate(name)#captura el co2 de los equipos heater
                heater_usage = self.sim.BLK_HEATER_Get_utility_usage(name)#captura el usage de los equipos heater

                datos[name]['co2'] = heater_co2rate
                datos[name]['usage'] = heater_usage
            elif typ == 'Compr':
                compr_co2rate = self.sim.BLK_COMPR_Get_utility_co2rate(name)
                compr_usage = self.sim.BLK_COMPR_Get_utility_usage(name)

                datos[name]['co2'] = compr_co2rate
                datos[name]['usage'] = compr_usage

                
        return sum(datos.values())


if __name__=="__main__":

    # initialize the thread pool and create the runner
    """n_proccess = 1
    pool = multiprocessing.Pool(n_proccess)
    runner = StarmapParallelization(pool.starmap)

    my_problem = MyOptimizationProblem(elementwise_runner=runner)"""
    my_problem = MyOptimizationProblem()
    algorithm = NSGA2(pop_size=80,
                 crossover=SBX(eta=11, prob=0.9),
                 mutation=PM(eta=10))

    result = minimize(my_problem,
                    algorithm,
                    ('n_gen', 80),
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



