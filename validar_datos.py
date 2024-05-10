from CodeLibrary import Simulation
import matplotlib.pyplot as plt
import random
import gc
import time
import pandas as pd


#############################
#apertura de datos
#############################
data = pd.read_csv("random_data.csv", sep=",", decimal=".")
flujo = []

#############################
#conexion
#############################
ini = time.time()
sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/midia/OneDrive/Escritorio/pablo" ,VISIBILITY=False)
fin = time.time()
print("\n tiempo de conexion: ",fin-ini)


datos_viables = pd.DataFrame(columns=['Presion', 'Temperatura', 'Peso', 'Flujo', 'H2', 'Hidrogeno', 'Metanol'])

for index, row in data.iterrows():
    sim.BLK_RPLUG_Set_InletProcessflowPressure("R-1",row["Presion"]) #asigna la presion del reactor R-1
    sim.BLK_RPLUG_Set_T_SPEC_Constant_Temp("R-1", row["Temperatura"]) #asigna la temperatura del raactor R-1
    sim.BLK_RPLUG_Set_WeightOfCatalystLoaded("R-1",row["Peso"]) #asigna el peso del reactor R-1
    sim.BLK_RADFRAC_Set_Refluxratio("COLUMN2", row["Flujo"]) #asigna la relacion de reflujo de la columna 2
    sim.h2(row["H2"]) # Asigna un valor de entrada para el total flow rate del H2 (metodo creado)
    sim.purge(row["Hidrogeno"]) #asignar la relacion de hidrogeno

    convergence = sim.Run()
    sim.DialogSuppression(TrueOrFalse= False)

    massFlow_metoh = sim.AspenSimulation.Tree.FindNode("\\Data\\Streams\\METOH\\Output\\MASSFLOW\\MIXED\\CH3OH").Value #capturar el flujo de metanol
    if convergence != False and massFlow_metoh != 0:
        row = list(row)
        row.append(massFlow_metoh)
        print(row)
        datos_viables.loc[len(datos_viables)] = row
        print(row)

datos_viables.to_csv("C:/Users/midia/OneDrive/Escritorio/code/pymoo/datos_viables.csv",decimal=',')

