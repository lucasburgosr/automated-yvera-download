import pandas as pd

df_regulares = pd.read_csv("./descargas/conectividad_terrestre_mendoza_regulares.csv", sep=",", low_memory=False)

df_regulares["Tipo"] = "SERVICIOS REGULARES"

df_regulares.to_csv("./descargas/conectividad_terrestre_mendoza_regulares.csv", sep=";", index=False)

df_turistico = pd.read_csv("./descargas/conectividad_terrestre_mendoza_turistico.csv", sep=",", low_memory=False)

df_turistico["Tipo"] = "SERVICIOS DE TURISMO"

df_turistico.to_csv("./descargas/conectividad_terrestre_mendoza_turistico.csv", sep=";", index=False)

df_regulares = pd.read_csv("./descargas/conectividad_terrestre_mendoza_regulares.csv", sep=";", low_memory=False)
df_turistico = pd.read_csv("./descargas/conectividad_terrestre_mendoza_turistico.csv", sep=";", low_memory=False)

df_final = pd.concat([df_regulares, df_turistico], axis=0)

df_final.to_csv("./descargas/conectividad_terrestre_mendoza_unificado.csv", sep=";", index=False)