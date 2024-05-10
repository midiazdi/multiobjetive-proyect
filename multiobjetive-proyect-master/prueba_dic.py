import pandas as pd
import numpy as np

df = pd.read_csv("./resultados.csv")

df = df.iloc[:,1:7]

import pandas as pd

# Supongamos que tienes un DataFrame llamado df y has definido los valores mínimos y máximos para cada columna
# Puedes definirlos como un diccionario donde las claves son los nombres de las columnas y los valores son tuplas (min, max)
valores_minimos_maximos = {
    'Presion': (10,120),
    'Temperatura': (190,300),
    'Peso':(10,10000),
    'Flujo':(0.1,4.5),
    'H2':(2500,75000),
    'Hidrogeno':(0.1,0.97)

}

# Normaliza cada columna aplicando la fórmula con los valores mínimos y máximos definidos
for columna, (minimo, maximo) in valores_minimos_maximos.items():
    df[columna] = (df[columna] - minimo) / (maximo - minimo)



df.to_csv("resultados_normalizados.csv")



