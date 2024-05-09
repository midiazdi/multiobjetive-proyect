import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
data = pd.read_csv("resultados")



import matplotlib.pyplot as plt
import pandas as pd

# Cargar los datos
data = pd.read_csv("resultados")  # Asegúrate de que el archivo se llame correctamente

# Variables a comparar con Consumo E y Energía, excluyéndolas de la comparación
variables1 = ['Presion', 'Temperatura', 'Peso']
variables2= ['Flujo', 'H2', 'Hidrogeno']
nombres1 = ['PRES1','TEM1', 'WEI']
nombres2 = ['RR', 'H2', 'BR']

# Primera figura: Variables vs Consumo E
fig1, axs1 = plt.subplots(3, 2, figsize=(5, 10))
for i, var in enumerate(variables1):
    # Variables con Consumo E
    axs1[i, 0].scatter(data['Metanol'],data[var],facecolors='none', edgecolors='black', alpha=0.5)
    axs1[i,0].plot(1821.86078,data.iloc[12][variables1[i]],'ro')
    #axs1[i, 0].set_title(f"{nombres1[i]} vs CE", fontsize=8)
    if i ==2:
        axs1[i,0].set_xlabel("UM")
    axs1[i,0].set_ylabel(f"{nombres1[i]}")
    axs1[i,0].tick_params(axis='x', labelsize=5)
    axs1[i,0].tick_params(axis='y', labelsize=5)


    axs1[i, 1].scatter(data['Metanol'],data[variables2[i]], facecolors='none', edgecolors='black', alpha=0.5 )
    axs1[i,1].plot(1821.86078,data.iloc[12][variables2[i]],'ro')
    if i ==2:
        axs1[i,1].set_xlabel("UM")
    axs1[i,1].set_ylabel(f"{nombres2[i]}")
    # Variables con Energía
    #axs1[i, 1].scatter(data[var], data['Consumo E'])
    #axs1[i, 1].set_title(f"{var} vs Consumo E")
    axs1[i,1].tick_params(axis='x', labelsize=5)
    axs1[i,1].tick_params(axis='y', labelsize=5)

# Ajustar para que no se superpongan los títulos

plt.tight_layout()
plt.show()

plt.scatter( data['Metanol'],data['Energia'], facecolors='none', edgecolors='black', alpha=0.5)
plt.plot(1821.86078,1862477.8, 'ro')
plt.annotate("""Punto Extremo """, # texto de la etiqueta
             (1821.86078,1862477.8),             # punto que queremos etiquetar
             textcoords="offset points", # cómo se posicionará el texto
             xytext=(-100,60),    # distancia del texto al punto (x,y)
             ha='center',        # alineación horizontal del texto
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2"))

plt.title("Frente de pareto")
plt.xlabel("Flujo de metanol m3/h")
plt.ylabel("Consumo Energético MJ/h")
plt.grid(True, which='both', axis='both', color='gray', linestyle='--', linewidth=0.5)
plt.show()


"""
# Crear una figura
fig = plt.figure()

# Añadir un subplot 3D
ax = fig.add_subplot(111, projection='3d')

# Gráfico de dispersión
ax.scatter(data["Consumo E"], data["Consumo E"], data["Peso"], alpha=0.5, edgecolors='black', facecolors='none')

# Títulos y etiquetas
ax.set_title('Gráfico de Dispersión 3D')
ax.set_xlabel('Eje X')
ax.set_ylabel('Eje Y')
ax.set_zlabel('Eje Z')

# Mostrar el gráfico"""

#en