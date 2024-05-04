import pandas as pd


dt = pd.read_csv('resultados.csv')

dt.to_csv('result',sep=';')
