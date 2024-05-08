from CodeLibrary import Simulation



sim = Simulation(AspenFileName= "Methanol_CO2.bkp", WorkingDirectoryPath= r"C:/Users/LAB-4066294/Desktop/Miguel/simulaciones" ,VISIBILITY=False)
convergence = sim.Run()
sim.DialogSuppression(TrueOrFalse= False)
#utl = sim.AspenSimulation.Tree.FindNode("\\Data\\Blocks\\COLUMN2\\Output\\UTL_PADUTY").Value
profit = sim.ListBlocks()

for name,typ in profit.items():
    print(name,typ)


datos = {
    'HEATER-1': 'LPSTEAM',
    'COMP-1':'EL',
    'COMP-3':'EL',
    'COMP-4':'EL',
    'COOLER-1':'WATER',
    'COOLER-2':'WATER',
    'COOLER-3':'WATER',
    'COOLER-4':'WATER',
    'COOLER-5':'WATER',
    'COOLER-6':'WATER',
    'COOLER-7':'WATER',
    'FLASH-1':'WATER',
    'FLASH-3':'WATER',
    'COLUMN1': 'WATER',
    'COLUMN1':'MPSTEAM',
    'COLUMN2': 'WATER',
    'COLUMN2':'MPSTEAM',

}