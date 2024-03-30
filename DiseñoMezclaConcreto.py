import pandas as pd
import numpy as np

def resistencia_requerida(resistencia_diseño):
    if resistencia_diseño < 210:
        return resistencia_diseño + 70
    elif  210 <=resistencia_diseño and resistencia_diseño <= 350: 
        return resistencia_diseño + 85
    else:
        return resistencia_diseño + 100
    
#Calculando la resistencia requerida segun ACI 318 2005
resistencia_diseño = 210    
resistencia_requerida = (resistencia_requerida(resistencia_diseño))
print("La resistencia requerida es:",resistencia_requerida)

#Datos de entrada de ensayos realizados a los agregados
datos = {
    "PESO ESPECIFICO": [3150, 2400, 2600],
    "MODULO DE FINURA": [0, 2.7, 0],
    "HUMEDAD NATURAL": [0, 8.15, 0.50],
    "PORCENTAJE DE ABSORCION": [0, 4.90, 1.92],
    "PESO SECO SUELTO": [0, 1384.04, 1377.98],
    "PESO SECO COMPACTADO": [0, 1509.93, 1455],
    "TAMAÑO MAXIMO NOMINAL": ['0', '0', '3/8']#Lo colcoamos entre comillas simples para que pandas lo reconozca
}

A = pd.DataFrame(datos, index=['CEMENTO', 'AGREGADO FINO', 'AGREGADO GRUESO'])
print(A)

#Tabla para calcular el aire atrapado en funcion al Tamaño Maximo Nominal
tabla_aire_atrapado = {
    "Tamaño Maximo Nominal": ['3/8', '1/2', '3/4', '1', '1.5', '2', '3', '6'],
    "Aire Atrapado": [3, 2.5, 2, 1.5, 1, 0.5, 0.3, 0.2 ]
}

B = pd.DataFrame(tabla_aire_atrapado, index=['1', '2', '3', '4', '5', '6', '7', '8'])
print(B)

# Tabla para calcular la relacion agua-cemento en funcion a la Resistencia Requerida
tabla_agua_cemento = {
    "Resistencia Requerida": [150, 200, 250, 300, 350, 400, 450],
    "Concreto sin Aire Incorporado": [0.8, 0.7, 0.62, 0.55, 0.48, 0.43, 0.38],
    "Concreto con Aire Incorporado": [0.71, 0.61, 0.53, 0.46, 0.40, 0.0, 0.0]
}

C = pd.DataFrame(tabla_agua_cemento, index=['1', '2', '3', '4', '5', '6', '7'])
print(C)

concreto_sin_aire_incorporado = True
Slump= '3 A 4'
Modulo_Finura= 2.7

#Tabla para calcular el volumen de agua para conreto sin aire incorporado
tabla_agua_concreto_sin_aire_incorporado = {
    '3/8': [207, 228, 243],
    '1/2': [199, 216, 228],
    '3/4': [190, 205, 216],
    '1': [179, 193, 202],
    '1.5': [166, 181, 190],
    '2': [154, 169, 178],
    '3': [130, 145, 160],
    '6': [113, 124, 0],
}


D = pd.DataFrame(tabla_agua_concreto_sin_aire_incorporado, index=['1 A 2', '3 A 4', '6 A 7'])
print(D)


#Tabla para calcular el volumen de agua para conreto con aire incorporado en funcion al Tamaño Maximo Nominal y al Slump
tabla_agua_concreto_con_aire_incorporado = {
    '3/8': [181, 202, 216],
    '1/2': [175, 193, 205],
    '3/4': [168, 184, 197],
    '1': [160, 175, 184],
    '1.5': [150, 165, 174],
    '2': [142, 157, 166],
    '3': [122, 133, 154],
    '6': [107, 119, 0],
}

F = pd.DataFrame(tabla_agua_concreto_con_aire_incorporado, index=['1 A 2', '3 A 4', '6 A 7'])
print(F)

# Tabla para calcular el volumen de agregado grueso seco compactado, en funcion al tamaño maximo nominal del agregado grueso y al modulo de fineza del agregado fino.

tabla_peso_agregado_unidad_volumen_concreto = {
    2.40: [0.50, 0.59, 0.66, 0.71, 0.76, 0.78, 0.81, 0.87],
    2.60: [0.48, 0.57, 0.64, 0.69, 0.74, 0.76, 0.79, 0.85],
    2.80: [0.46, 0.55, 0.62, 0.67, 0.72, 0.74, 0.77, 0.83],
    3.00: [0.44, 0.53, 0.60, 0.65, 0.70, 0.72, 0.75, 0.81]
}

G = pd.DataFrame(tabla_peso_agregado_unidad_volumen_concreto, index=['3/8', '1/2', '3/4', '1', '1.5', '2', '3', '6'])
print(G)



# Capturando datos de las tablas ACI 211 
# Buscar el tamaño máximo nominal del agregado grueso para eso usamos el atributo "loc"(Tabla A)
tamano_max_nominal_agregado_grueso = A.loc['AGREGADO GRUESO', 'TAMAÑO MAXIMO NOMINAL']
#print("Tamaño máximo nominal del agregado grueso:", tamano_max_nominal_agregado_grueso)
peso_especifico_cemento = A.loc['CEMENTO', 'PESO ESPECIFICO']
#print("Peso especifico del cemento es:", peso_especifico_cemento)
peso_especifico_agregado_fino = A.loc['AGREGADO FINO', 'PESO ESPECIFICO']
#print("Peso especifico del agregado fino es:", peso_especifico_agregado_fino)
peso_especifico_agregado_grueso = A.loc['AGREGADO GRUESO', 'PESO ESPECIFICO']
#print("Peso especifico del agregado grueso es:", peso_especifico_agregado_grueso)
peso_suelto_agregado_fino = A.loc['AGREGADO FINO', 'PESO SECO SUELTO']
#print("Peso seco suelto del agregado fino es:", peso_suelto_agregado_fino)
peso_suelto_agregado_grueso = A.loc['AGREGADO GRUESO', 'PESO SECO SUELTO']
#print("Peso seco suelto del agregado agregado es:", peso_suelto_agregado_grueso)
peso_seco_compactado_agregado_grueso = A.loc['AGREGADO GRUESO', 'PESO SECO COMPACTADO']
#print("Peso seco compactado del agregado grueso es:", peso_seco_compactado_agregado_grueso)
humedad_agregado_fino = A.loc['AGREGADO FINO', 'HUMEDAD NATURAL']
#print("Humedad natural del agregado fino es:", humedad_agregado_fino)
humedad_agregado_grueso = A.loc['AGREGADO GRUESO', 'HUMEDAD NATURAL']
#print("Humedad natural del agregado grueso es:", humedad_agregado_grueso)
porcentaje_absorcion_fino = A.loc['AGREGADO FINO', 'PORCENTAJE DE ABSORCION']
#print("Porcentaje de absorcion del agregado fino es:", porcentaje_absorcion_fino)
porcentaje_absorcion_grueso = A.loc['AGREGADO GRUESO', 'PORCENTAJE DE ABSORCION']
#print("Porcentaje de absorcion del agregado grueso es:", porcentaje_absorcion_grueso)


# Optenemos el aire atrapado en funcion al tamaño maximo nominal (Tabla B)
if tamano_max_nominal_agregado_grueso in B["Tamaño Maximo Nominal"].values:
    aire_atrapado = B.loc[B["Tamaño Maximo Nominal"] == tamano_max_nominal_agregado_grueso, "Aire Atrapado"].values[0]
    print("El valor correspondiente de Aire Atrapado es:", aire_atrapado)
else:
    print("No se encontró una coincidencia para el tamaño máximo nominal del agregado grueso en la tabla de aire atrapado.")

# Optenemos la relacion agua - cemento en funcion a la resistencia requerida (Tabla C)
if concreto_sin_aire_incorporado:
    columna_a_utilizar = 'Concreto sin Aire Incorporado'
else:
    columna_a_utilizar = 'Concreto con Aire Incoprorado'

relacion_agua_cemento = np.interp(resistencia_requerida, C['Resistencia Requerida'], C[columna_a_utilizar])
#print("Relacion agua-cemento de 'Concreto sin Aire Incorporado' es:", relacion_agua_cemento)


# Obtenemos el volumen de agua en funcion al tamaño maximo nominal y al slump (Tablas D y F)
if concreto_sin_aire_incorporado:
    tabla_agua = D  # Usar la tabla tabla_agua_concreto_sin_aire_incorporado
else:
    tabla_agua = F  # Usar la tabla tabla_agua_concreto_con_aire_incorporado

if Slump in tabla_agua.index and tamano_max_nominal_agregado_grueso in tabla_agua.columns:
    volumen_agua = tabla_agua.loc[Slump, tamano_max_nominal_agregado_grueso]
    #print("El volumen de agua es:", volumen_agua)
else:
    print("No se encontró una coincidencia en la tabla de volumen de agua para los valores proporcionados.")


#Obtenemos el volumen de agregado grueso seco compactado en funcion al modulo de fineza del agregado fino y del tamañ maximo nominal del agregado grueso (Tabla G)
# Verificar si el Modulo_Finura está en la tabla_peso_agregado_unidad_volumen_concreto
if tamano_max_nominal_agregado_grueso in G.index and Modulo_Finura in G.columns:
    # Obtener el valor correspondiente directamente
    volumen_agregado_sin_interporlar = G.loc[tamano_max_nominal_agregado_grueso, Modulo_Finura]
    print("El volumen de agregado grueso compactado es:", volumen_agregado_sin_interporlar)
else:
    # Si no se encuentra una coincidencia directa, realizar interpolación
    # Encontrar los valores de Modulo_Finura más cercanos en la tabla
    nearest_below = G.columns[G.columns < Modulo_Finura][-1]
    nearest_above = G.columns[G.columns > Modulo_Finura][0]
    # Realizar interpolación lineal
    volumen_agregado_con_interporlar = np.interp(
        Modulo_Finura, [nearest_below, nearest_above], [G.loc[tamano_max_nominal_agregado_grueso, nearest_below], G.loc[tamano_max_nominal_agregado_grueso, nearest_above]]
    )
    print("El volumen de agregado grueso compactado es:", volumen_agregado_con_interporlar )



#Realizando los calculos respectivo
    
# Con la relacion agua cemento calculamos el contenido de cemento ya que conocemos el volumen de agua.
peso_cemento = round(volumen_agua/relacion_agua_cemento,2)
print("Peso de cemento es:", peso_cemento)

# Calculamos el Peso del Agregado grueso para lo cual usaremos el volumen de agregado grueso, si volumen_agregado_sin_interporlar es false es porque se tuvo que interpolar y por eso trabajara con volumen_agregado_con_interporlar
volumen_agregado_sin_interporlar = False

if volumen_agregado_sin_interporlar:
    peso_agregado_grueso = round(volumen_agregado_sin_interporlar * peso_seco_compactado_agregado_grueso, 2)
    print("El peso del agregado grueso es:", peso_agregado_grueso )

else:
    peso_agregado_grueso = round(volumen_agregado_con_interporlar * peso_seco_compactado_agregado_grueso, 2)
    print("El peso del agregado grueso es:", peso_agregado_grueso )



# Calculamos el Volumen Absoluto
vol_cemento = round(peso_cemento /peso_especifico_cemento, 3)
print("El volumen del cemento es:", vol_cemento )
vol_agua = round(volumen_agua /1000, 3)
print("El volumen del agua es:", vol_agua)
vol_aire = round(aire_atrapado /100, 3)
print("El volumen del aire es:", vol_aire)
vol_agregado_grueso = round(peso_agregado_grueso /peso_especifico_agregado_grueso, 3)
print("El volumen del agregado grueso es:", vol_agregado_grueso)
vol_parcial = round((vol_cemento + vol_agua + vol_aire + vol_agregado_grueso), 3)
print("El volumen parcial es:", vol_parcial)
vol_agregado_fino = round((1 - vol_parcial), 3)
print("El volumen del agregado fino es:", vol_agregado_fino)


# Calculamos el Peso del Agregafo Fino a partir de su respectivo volumen
peso_agregado_fino = round((vol_agregado_fino * peso_especifico_agregado_fino),3)
print("El peso del agregado fino es:", peso_agregado_fino )


# Correcion por Humedad de lo agregados
peso_agregado_fino_corr = round((peso_agregado_fino * (1 + humedad_agregado_fino/100)), 3)
print("El peso del agregado fino corregido es:", peso_agregado_fino_corr )
peso_agregado_grueso_corr = round((peso_agregado_grueso * (1 + humedad_agregado_grueso/100)), 3)
print("El peso del agregado grueso corregido es:", peso_agregado_grueso_corr )

#Aporte de agua libre de los agregados
aporte_agua_agregado_fino = round((peso_agregado_fino * (humedad_agregado_fino - porcentaje_absorcion_fino)/100), 3)
print("El aporte de agua del agregado fino es:", aporte_agua_agregado_fino)

aporte_agua_agregado_grueso = round((peso_agregado_grueso * (humedad_agregado_grueso - porcentaje_absorcion_grueso)/100), 3)
print("El aporte de agua del agregado fino es:", aporte_agua_agregado_grueso)


# Agua de Diseño
agua_diseño = round((volumen_agua - (aporte_agua_agregado_fino + aporte_agua_agregado_grueso)), 3)
print("El agua de diseño sera:", agua_diseño)


#Correcion del Peso Unitario Suelto del agregado grueso y agregado fino en funcion al contenido de humendad, debido a que en laboratorio el ensayo se realiza en condicion seco, mientras que en obra los agregados estaran humedos.

peso_unitario_suelto_fino_corr = round((peso_suelto_agregado_fino*(1 + humedad_agregado_fino/100)), 3)
peso_unitario_suelto_grueso_corr = round((peso_suelto_agregado_grueso*(1 + humedad_agregado_grueso/100)), 3)


# I) Cantidad de Materiales corregidas por humedad o Peso Obra (W.O)
peso_obra_cemento = peso_cemento
peso_obra_agua = agua_diseño
peso_obra_agregado_fino = peso_agregado_fino_corr
peso_obra_agregado_grueso = peso_agregado_grueso_corr

#Almacenando los valores en un dataframe
# Definir los valores
valores_obra = {
    "cemento": peso_obra_cemento,
    "agua": peso_obra_agua,
    "agregado_fino": peso_obra_agregado_fino,
    "agregado_grueso": peso_obra_agregado_grueso
}

# Crear el DataFrame
peso_materiales_obra = pd.DataFrame(valores_obra, index=["Cantidad"])

# Agregar el título
peso_materiales_obra.columns.name = "PESO OBRA (W.O)"

print(peso_materiales_obra)



# II) Calculamos el Peso Unitario de Obra (W.U.O)

peso_unitario_cemento = peso_obra_cemento/peso_obra_cemento
peso_unitario_agua = round((peso_obra_agua/peso_obra_cemento), 2)
peso_unitario_agregado_fino = round((peso_obra_agregado_fino/peso_obra_cemento), 2)
peso_unitario_agregado_grueso = round((peso_obra_agregado_grueso/peso_obra_cemento), 2)

# Almacenando los valores en un dataframe
# Definir los valores
valores_unitario = {
    "cemento": peso_unitario_cemento,
    "agua": peso_unitario_agua,
    "agregado_fino": peso_unitario_agregado_fino,
    "agregado_grueso": peso_unitario_agregado_grueso
}


# Crear el DataFrame
peso_unitario_materiales = pd.DataFrame(valores_unitario, index=["Cantidad"])

# Agregar el título
peso_unitario_materiales.columns.name = "PROPORCION EN PESO"

print(peso_unitario_materiales)


# Calculamos la proporcion de materiales x bolsa de cemento de 42.5 kg

propocion_cemento_bolsa = peso_unitario_cemento * 42.5
proporcion_agua_bolsa = round((peso_unitario_agua * 42.5), 2)
proporcion_fino_bolsa = round((peso_unitario_agregado_fino * 42.5), 2)
proporcion_grueso_bolsa = round((peso_unitario_agregado_grueso * 42.5), 2)



# III) Calculamos la proporcion en Volumen Aparente en pies cubicos

vol_cemento_pie_cubico = peso_unitario_cemento/peso_unitario_cemento
vol_agua_pie_cubico = proporcion_agua_bolsa
vol_agregado_fino_pie_cubico = round((proporcion_fino_bolsa*35.31/peso_unitario_suelto_fino_corr), 2)
vol_agregado_grueso_pie_cubico = round((proporcion_grueso_bolsa*35.31/peso_unitario_suelto_grueso_corr), 2)

# Almacenando los valores en un dataframe
# Definir los valores
valores_pie_cubico = {
    "cemento": vol_cemento_pie_cubico,
    "agua": vol_agua_pie_cubico,
    "agregado_fino": vol_agregado_fino_pie_cubico,
    "agregado_grueso": vol_agregado_grueso_pie_cubico
}

# Crear el DataFrame
volumen_materiales_pie_cubico = pd.DataFrame(valores_pie_cubico, index=["Volumen"])

# Agregar el título
volumen_materiales_pie_cubico.columns.name = "PROPORCION VOLUMEN EN PIES CUBICOS"

print(volumen_materiales_pie_cubico)



