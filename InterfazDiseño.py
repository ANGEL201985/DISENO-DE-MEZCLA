import sys  # Importa el módulo sys, que proporciona acceso a algunas variables utilizadas o mantenidas por el intérprete y a funciones que interactúan fuertemente con el intérprete.
import numpy as np  # Importa el módulo numpy y lo renombra como np. NumPy es una biblioteca para el lenguaje de programación Python, que soporta matrices y matrices multidimensionales, junto con una amplia colección de funciones matemáticas.
import pandas as pd  # Importa el módulo pandas y lo renombra como pd. Pandas es una biblioteca de código abierto que proporciona estructuras de datos de alto rendimiento y fáciles de usar y herramientas de análisis de datos para el lenguaje de programación Python.
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, QRadioButton  # Importa clases específicas de PyQt6.QtWidgets necesarias para la interfaz gráfica.
from PyQt6.QtGui import QFont, QIcon  # Importa clases específicas de PyQt6.QtGui necesarias para la interfaz gráfica.
from PyQt6.QtCore import Qt  # Importa clases específicas de PyQt6.QtCore necesarias para la interfaz gráfica.
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextBrowser # Esta clase QTextBrowser lo usamos para trabajar con la tabla HTML
from fractions import Fraction



# Definición de la clase MainWindow, que hereda de QMainWindow. La ventana principal que has definido como MainWindow es la interfaz gráfica principal de tu aplicación. Esta ventana es la que contendrá todos los elementos de la interfaz de usuario que has diseñado, como botones, etiquetas, cuadros de texto, etc. Es la parte central de tu aplicación donde los usuarios interactuarán y verán los resultados de las acciones que realicen. MainWindow es una clase del cual podemos instanciar nuevos objetos

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("Diseño de Mezcla de Concreto developed by Angel Ramos Vila")
        self.setWindowIcon(QIcon('carretera.png'))
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("DISEÑO DE MEZCLA DE CONCRETO ACI - 211", alignment=Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: blue; font-size: 16px; font-weight: bold;")
        title_label.setMaximumHeight(20)
        main_layout.addWidget(title_label)

        
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(["P.E (kg/m3)", "M.F", "% W", "% ABS", "P.U.S (kg/m3)", "P.U.C (kg/m3)", "TMN"])
        row_height = self.tableWidget.verticalHeader().defaultSectionSize()
        self.tableWidget.setFixedHeight(3 * row_height + self.tableWidget.horizontalHeader().height() + 5) # Ajustamos la altura de nuestra tabla donde ingresamos los datos
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignHCenter)
        main_layout.addWidget(self.tableWidget, stretch=1)

        self.tableWidget.setVerticalHeaderLabels(["CEMENTO", "AGREGADO FINO", "AGREGADO GRUESO"])

        for i in range(3):
            for j in range(7):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.tableWidget.setItem(i, j, item)

        self.resistencia_label = QLabel("Resistencia de Diseño (kg/cm2):")
        self.resistencia_input = QLineEdit()  # Usar self.resistencia_input en lugar de resistencia_input
       
        self.slump_label = QLabel("Ingrese Slump:")
        self.slump_input = QLineEdit()  # Usar self.resistencia_input en lugar de resistencia_input

        #Crear Label para botones radio
        
        self.radio_sin_aire_label = QLabel("Concreto sin aire incorporado")
        self.radio_con_aire_label = QLabel("Concreto con aire incorporado")
         #Crear botones de radio
        self.radio_sin_aire = QRadioButton()
        self.radio_con_aire = QRadioButton()
        self.radio_sin_aire.setChecked(False)  # Establecer el estado inicial en False
        self.radio_con_aire.setChecked(False)  # Establecer el estado inicial en False

        # Conectar la señal toggled de los botones de radio a la función correspondiente
        self.radio_sin_aire.toggled.connect(self.desactivar_botones_radio)
        self.radio_con_aire.toggled.connect(self.desactivar_botones_radio)

         
        # Agregar un QLabel para mostrar el valor de "Aire Atrapado"
        self.aire_atrapado_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)


        # Agrega el botón para calcular el aire atrapado
        calcular_aire_button = QPushButton("Aire Atrapado (%)", clicked=self.calcularAireAtrapado)
        

        # Crear un QHBoxLayout para contener los widgets relacionados con la resistencia
        calculo1_layout = QHBoxLayout()
        calculo1_layout.addWidget(self.resistencia_label)
        calculo1_layout.addWidget(self.resistencia_input)
        calculo1_layout.addWidget(self.slump_label)
        calculo1_layout.addWidget(self.slump_input)
        calculo1_layout.addWidget(self.radio_sin_aire)
        calculo1_layout.addWidget(self.radio_sin_aire_label)
        calculo1_layout.addWidget(self.radio_con_aire)
        calculo1_layout.addWidget(self.radio_con_aire_label)

       
        calcular_resistencia_requerida = QPushButton("Resistencia Requerida (kg/cm2)", clicked=self.calcularResistencia)
        self.resistencia_requerida_label = QLabel()

        # Agregar un QLabel para mostrar la relación agua-cemento sin aire
        self.relacion_agua_cemento_sin_aire_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.relacion_agua_cemento_sin_aire_label)

        # Agregar un QLabel para mostrar la relación agua-cemento con aire
        self.relacion_agua_cemento_con_aire_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(self.relacion_agua_cemento_con_aire_label)

         # Agrega el botón para calcular el aire atrapado
        calcular_agua_cemento = QPushButton("Relacion Agua - Cemento", clicked=self.calcularRelacionAguaCemento)

        
        # Agregar un QLabel para mostrar el valor el "Volumen de Agua"
        self.volumen_agua_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el aire atrapado
        calcular_volumen_agua = QPushButton("Volumen Agua (lt)", clicked=self.calcularVolumenAgua)

        # Agregar un QLabel para mostrar el valor el "Volumen de agregado grueso"
        self.volumen_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el aire atrapado
        calcular_volumen_agregado_grueso = QPushButton("Volumen Agregado Grueso", clicked=self.calcularVolumenAgregadoGrueso)

        
        # Crear un QHBoxLayout para contener los widgets relacionados a calculos 2 esto basicamente hace que los checkRadio, el boton de calcular agua-cemento y el texto Relacion agua-cemento con aire o sin aire aparezcan en una sola lina
        calculo2_layout = QHBoxLayout()
        calculo2_layout.addWidget(calcular_resistencia_requerida)
        calculo2_layout.addWidget(self.resistencia_requerida_label)
        calculo2_layout.addWidget(calcular_aire_button)
        calculo2_layout.addWidget(self.aire_atrapado_label)      
        calculo2_layout.addWidget(calcular_agua_cemento)
        calculo2_layout.addWidget(self.relacion_agua_cemento_con_aire_label)
        calculo2_layout.addWidget(self.relacion_agua_cemento_sin_aire_label)
        calculo2_layout.addWidget(calcular_volumen_agua)
        calculo2_layout.addWidget(self.volumen_agua_label)
        calculo2_layout.addWidget(calcular_volumen_agregado_grueso)
        calculo2_layout.addWidget(self.volumen_agregado_grueso_label)
        

         # Agregar un QLabel para mostrar el valor el "Peso del Cemento"
        self.peso_cemento_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Peso del Cemento
        calcular_peso_cemento = QPushButton("Contenido Cemento (kg/m3)", clicked=self.calcularPesoCemento)

         # Agregar un QLabel para mostrar el valor el "Peso del Agregado Grueso"
        self.peso_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Peso del Agregado Grueso
        calcular_peso_agregado_grueso = QPushButton("Peso Agregado Grueso (kg/m3)", clicked=self.calcularPesoAgregadoGrueso)

        # Agregar un QLabel para mostrar el valor el "Volumen de cemento"
        self.volumen_cemento_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Volumen de cemento
        calcular_volumen_cemento = QPushButton("Volumen Absoluto Cemento (m3)", clicked=self.volumenCemento)
        
        # Agregar un QLabel para mostrar el valor el "Volumen absoluto de agua"
        self.volumen_agua_absoluto_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Volumen absoluto de agua
        calcular_volumen_agua_absoluto = QPushButton("Volumen Absoluto Agua (m3)", clicked=self.volumenAguaAbsoluto)

        calculo3_layout = QHBoxLayout()
        calculo3_layout.addWidget(calcular_peso_cemento)
        calculo3_layout.addWidget(self.peso_cemento_label)
        calculo3_layout.addWidget(calcular_peso_agregado_grueso)
        calculo3_layout.addWidget(self.peso_agregado_grueso_label)
        calculo3_layout.addWidget(calcular_volumen_cemento)
        calculo3_layout.addWidget(self.volumen_cemento_label)
        calculo3_layout.addWidget(calcular_volumen_agua_absoluto)
        calculo3_layout.addWidget(self.volumen_agua_absoluto_label)

        # Agregar un QLabel para mostrar el valor el "Volumen absoluto de aire"
        self.volumen_aire_absoluto_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Volumen absoluto de aire
        calcular_volumen_aire_absoluto = QPushButton("Volumen Absoluto Aire (m3)", clicked=self.volumenAireAbsoluto)

         # Agregar un QLabel para mostrar el valor el "Volumen absoluto de agregado grueso"
        self.volumen_absoluto_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Volumen absoluto de agregado grueso
        calcular_volumen_agregado_grueso_absoluto = QPushButton("Volumen Absoluto Agregado Grueso (m3)", clicked=self.volumenAgregadoGruesoAbsoluto)

         # Agregar un QLabel para mostrar el valor el "Volumen absoluto de agregado fino"
        self.volumen_absoluto_agregado_fino_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el Volumen absoluto de agregado fino
        calcular_volumen_agregado_fino_absoluto = QPushButton("Volumen Absoluto Agregado Fino (m3)", clicked=self.volumenAgregadoFinoAbsoluto)

        # Agregar un QLabel para mostrar el valor el "peso de agregado fino"
        self.peso_agregado_fino_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el peso de agregado fino
        calcular_peso_agregado_fino = QPushButton("Peso Agregado Fino (kg/m3)", clicked=self.calcularPesoAgregadoFino)


        calculo4_layout = QHBoxLayout()
        calculo4_layout.addWidget(calcular_volumen_aire_absoluto)
        calculo4_layout.addWidget(self.volumen_aire_absoluto_label)
        calculo4_layout.addWidget(calcular_volumen_agregado_grueso_absoluto)
        calculo4_layout.addWidget(self.volumen_absoluto_agregado_grueso_label)
        calculo4_layout.addWidget(calcular_volumen_agregado_fino_absoluto)
        calculo4_layout.addWidget(self.volumen_absoluto_agregado_fino_label)
        calculo4_layout.addWidget(calcular_peso_agregado_fino)
        calculo4_layout.addWidget(self.peso_agregado_fino_label)


        # Agregar un QLabel para mostrar el valor el "peso de agregado grueso corregido"
        self.peso_agregado_grueso_corregido_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el peso de agregado grueso corregido
        calcular_peso_agregado_grueso_corregido = QPushButton("A.G Corregido Humedad (kg/m3)", clicked=self.agregadoGruesoCorr)

        # Agregar un QLabel para mostrar el valor el "peso de agregado fino corregido"
        self.peso_agregado_fino_corregido_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el peso de agregado fino corregido
        calcular_peso_agregado_fino_corregido = QPushButton("A.F Corregido Humedad (kg/m3)", clicked=self.agregadoFinoCorr)

        # Agregar un QLabel para mostrar el valor el "aporte de agregado grueso"
        self.aporte_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el aporte de agregado grueso
        calcular_aporte_agregado_grueso = QPushButton("Aporte Agregado Grueso (lt)", clicked=self.aporteagregadogrueso)

        # Agregar un QLabel para mostrar el valor el "aporte de agregado fino"
        self.aporte_agregado_fino_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para calcular el aporte de agregado fino
        calcular_aporte_agregado_fino = QPushButton("Aporte Agregado Fino (lt)", clicked=self.aporteagregadofino)

        calculo5_layout = QHBoxLayout()
        calculo5_layout.addWidget(calcular_peso_agregado_grueso_corregido)
        calculo5_layout.addWidget(self.peso_agregado_grueso_corregido_label)
        calculo5_layout.addWidget(calcular_peso_agregado_fino_corregido)
        calculo5_layout.addWidget(self.peso_agregado_fino_corregido_label)
        calculo5_layout.addWidget(calcular_aporte_agregado_grueso)
        calculo5_layout.addWidget(self.aporte_agregado_grueso_label)
        calculo5_layout.addWidget(calcular_aporte_agregado_fino)
        calculo5_layout.addWidget(self.aporte_agregado_fino_label)

        # Agregar un QLabel para mostrar la cantidad de cemento
        self.cantidad_cemento_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la cantidad de agua corregida
        self.cantidad_agua_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la cantidad de agregado grueso
        self.cantidad_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

         # Agregar un QLabel para mostrar la cantidad de agregado fino
        self.cantidad_agregado_fino_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

         # Agregar un QLabel para mostrar los resultados
        self.mostrar_resultado_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para mostrar los resultados
        mostrar_resultado = QPushButton("Cantidad Materiales", clicked=self.mostrarResultados)
        mostrar_resultado.setObjectName("CantidadMateriales")

        calculo6_layout = QVBoxLayout()
        calculo6_layout.addWidget(mostrar_resultado)
        calculo6_layout.addWidget(self.mostrar_resultado_label)
        calculo6_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centra horizontalmente el botón Cantidad de Materiales

        # Agregar un QLabel para mostrar la cantidad unitaria de cemento
        self.cantidad_cemento_unitario_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la cantidad unitaria de agua
        self.cantidad_agua_unitario_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la cantidad unitaria de agregado grueso
        self.cantidad_agregado_grueso_unitario_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

         # Agregar un QLabel para mostrar la cantidad unitaria de agregado fino
        self.cantidad_agregado_fino_unitario_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar los resultados de peso unitarios
        self.peso_obra_unitario_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para mostrar los resultados
        mostrar_resultado_unitarios = QPushButton("Proporcion en Peso", clicked=self.mostrarPesosUnitarios)
        mostrar_resultado_unitarios.setObjectName("PesoUnitario")

        
        calculo7_layout = QVBoxLayout()
        calculo7_layout.addWidget(mostrar_resultado_unitarios)
        calculo7_layout.addWidget(self.peso_obra_unitario_label)
        calculo7_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centra horizontalmente el botón Proporcion en Peso
       

        # Agregar un QLabel para mostrar la proporcion en volumen de cemento
        self.proporcion_volumen_cemento_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la proporcion volumen de agua
        self.porporcion_volumen_agua_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agregar un QLabel para mostrar la proporcion volumen de agregado grueso
        self.proporcion_volumen_agregado_grueso_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

         # Agregar un QLabel para mostrar la proporcion volumen de agregado fino
        self.proporcion_volumen_agregado_fino_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

         # Agregar un QLabel para mostrar los resultados de proporcion de volumenes
        self.proporcion_volumen_label = QLabel(alignment=Qt.AlignmentFlag.AlignCenter)

        # Agrega el botón para mostrar los resultados de proporcion de volumenes
        mostrar_proporcion_volumen = QPushButton("Proporcion en Volumen (pie cubico)", clicked=self.mostrarProporcionVolumen)
        mostrar_proporcion_volumen.setObjectName("ProporcionVolumen")

        calculo8_layout = QVBoxLayout()
        calculo8_layout.addWidget(mostrar_proporcion_volumen)
        calculo8_layout.addWidget(self.proporcion_volumen_label)
        calculo8_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  # Centra horizontalmente el botón Proporcion en Volumen
      
        # Los QVBoxLayout 7 y 8 lo agregaremos a un nuevo QHBoxLayout

        calculo9_layout = QHBoxLayout()
        # Agregar los layouts de las tablas a calculo9_layout
        calculo9_layout.addLayout(calculo7_layout)
        calculo9_layout.addLayout(calculo8_layout)
    
       # Crear el botón para limpiar la interfaz
        limpiar_datos = QPushButton("Limpiar Datos")
        limpiar_datos.setObjectName("limpiarButton")  # Asigna un nombre único al botón y con este nombre podemos seleccionarlo en Styles para agregarle estilos.
        limpiar_datos.clicked.connect(self.limpiarInterfaz)

        # Crear un layout horizontal para contener el botón
        boton_layout = QHBoxLayout()
        boton_layout.addWidget(limpiar_datos)

        # Agregar el layout horizontal que contiene el botón a tu diseño principal
        calculo10_layout = QHBoxLayout()
        calculo10_layout.addLayout(boton_layout)


        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo1_layout)

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo2_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo3_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo4_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo5_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo6_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo9_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Agregar el QHBoxLayout al QVBoxLayout principal
        main_layout.addLayout(calculo10_layout) # #Con main_layout agregamos la tabla a la interfaz grafica

        # Crear el widget de la tabla para aire atrapado
        tabla_aire_atrapado = {
            "TMN": ['3/8', '1/2', '3/4', '1', '1.5', '2', '3', '6'],
            "Aire Atrapado": [3, 2.5, 2, 1.5, 1, 0.5, 0.3, 0.2]
        }
        self.table_aire = QTableWidget()
        self.table_aire.setRowCount(len(tabla_aire_atrapado["TMN"]))
        self.table_aire.setColumnCount(len(tabla_aire_atrapado))
        self.table_aire.setHorizontalHeaderLabels(["TMN", "Aire Atrapado"])

        for i, (tamaño, aire) in enumerate(zip(tabla_aire_atrapado["TMN"], tabla_aire_atrapado["Aire Atrapado"])):
            self.table_aire.setItem(i, 0, QTableWidgetItem(tamaño))
            self.table_aire.setItem(i, 1, QTableWidgetItem(str(aire)))
            # Establecer alineación horizontal centrada para cada celda
            self.table_aire.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table_aire.item(i, 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        
        # Crear el widget de la tabla relacion agua - cemento

        tabla_agua_Cemento = {
            "f'cr": [150, 200, 250, 300, 350, 400, 450],
            "Concreto sin Aire Incorporado": [0.8, 0.7, 0.62, 0.55, 0.48, 0.43, 0.38],
            "Concreto con Aire Incorporado": [0.71, 0.61, 0.53, 0.46, 0.40, 0.0, 0.0]
        }

        self.table_agua_cemento = QTableWidget()
        self.table_agua_cemento.setRowCount(len(tabla_agua_Cemento["f'cr"]))
        self.table_agua_cemento.setColumnCount(len(tabla_agua_Cemento))
        self.table_agua_cemento.setHorizontalHeaderLabels(["f'cr", "Concreto sin Aire Incorporado", "Concreto con Aire Incorporado"])

        for i, (resistencia, aireIncorporado, sinAireIncorporado) in enumerate(zip(tabla_agua_Cemento["f'cr"], tabla_agua_Cemento["Concreto sin Aire Incorporado"], tabla_agua_Cemento["Concreto con Aire Incorporado"])):
            self.table_agua_cemento.setItem(i, 0, QTableWidgetItem(str(resistencia)))  # Convertir resistencia a cadena para que se muestre en nuestra tabla
            self.table_agua_cemento.setItem(i, 1, QTableWidgetItem(str(aireIncorporado)))
            self.table_agua_cemento.setItem(i, 2, QTableWidgetItem(str(sinAireIncorporado)))
            # Establecer alineación horizontal centrada para cada celda
            self.table_agua_cemento.item(i, 0).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table_agua_cemento.item(i, 1).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.table_agua_cemento.item(i, 2).setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)


        # Crear el widget de la tabla para volumen de agua sin aire incorporado
        self.tabla_agua_concreto_sin_aire_incorporado = pd.DataFrame({
            '3/8': [207, 228, 243],
            '1/2': [199, 216, 228],
            '3/4': [190, 205, 216],
            '1': [179, 193, 202],
            '1.5': [166, 181, 190],
            '2': [154, 169, 178],
            '3': [130, 145, 160],
            '6': [113, 124, 0],
        }, index=['1 A 2', '3 A 4', '6 A 7'])
       
        # Crear la tabla en PyQt6 para el calculo del volumen de agua
        self.table_agua_concreto_sin_aire = QTableWidget()
        self.table_agua_concreto_sin_aire.setRowCount(len(self.tabla_agua_concreto_sin_aire_incorporado.index))
        self.table_agua_concreto_sin_aire.setColumnCount(len(self.tabla_agua_concreto_sin_aire_incorporado.columns))
        self.table_agua_concreto_sin_aire.setHorizontalHeaderLabels(self.tabla_agua_concreto_sin_aire_incorporado.columns)

        # Llenar la tabla con los datos del DataFrame
        for i, row in enumerate(self.tabla_agua_concreto_sin_aire_incorporado.itertuples()):
            for j, value in enumerate(row[1:], start=0):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Establecer la alineación horizontal centrada de los elementos
                self.table_agua_concreto_sin_aire.setItem(i, j, item)

        self.table_agua_concreto_sin_aire.setVerticalHeaderLabels(self.tabla_agua_concreto_sin_aire_incorporado.index)
        
       
        # Crear el widget de la tabla para volumen de agua con aire incorporado
        self.tabla_agua_concreto_con_aire_incorporado = pd.DataFrame({
            '3/8': [181, 202, 216],
            '1/2': [175, 193, 205],
            '3/4': [168, 184, 197],
            '1': [160, 175, 184],
            '1.5': [150, 165, 174],
            '2': [142, 157, 166],
            '3': [122, 133, 154],
            '6': [107, 119, 0],
        }, index=['1 A 2', '3 A 4', '6 A 7'])
        
        # Crear la tabla en PyQt6
        self.table_agua_concreto_con_aire = QTableWidget()
        self.table_agua_concreto_con_aire.setRowCount(len(self.tabla_agua_concreto_con_aire_incorporado.index))
        self.table_agua_concreto_con_aire.setColumnCount(len(self.tabla_agua_concreto_con_aire_incorporado.columns))
        self.table_agua_concreto_con_aire.setHorizontalHeaderLabels(self.tabla_agua_concreto_con_aire_incorporado.columns)

        # Llenar la tabla con los datos del DataFrame
        for i, row in enumerate(self.tabla_agua_concreto_con_aire_incorporado.itertuples()):
            for j, value in enumerate(row[1:], start=0):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Establecer la alineación horizontal centrada de los elementos
                self.table_agua_concreto_con_aire.setItem(i, j, item)

        self.table_agua_concreto_con_aire.setVerticalHeaderLabels(self.tabla_agua_concreto_con_aire_incorporado.index)
        
        # Crear el widget PARA calcular el volumen de agregado grueso seco compactado, en funcion al tamaño maximo nominal del agregado grueso y al modulo de fineza del agregado fino.
        self.tabla_volumen_concreto_peso = pd.DataFrame({
            2.40: [0.50, 0.59, 0.66, 0.71, 0.76, 0.78, 0.81, 0.87],
            2.60: [0.48, 0.57, 0.64, 0.69, 0.74, 0.76, 0.79, 0.85],
            2.80: [0.46, 0.55, 0.62, 0.67, 0.72, 0.74, 0.77, 0.83],
            3.00: [0.44, 0.53, 0.60, 0.65, 0.70, 0.72, 0.75, 0.81]
        }, index=['3/8', '1/2', '3/4', '1', '1.5', '2', '3', '6'])

        # Crear la tabla en PyQt6
        self.tabla_volumen_concreto = QTableWidget()
        self.tabla_volumen_concreto.setRowCount(len(self.tabla_volumen_concreto_peso.index))
        self.tabla_volumen_concreto.setColumnCount(len(self.tabla_volumen_concreto_peso.columns))
        self.tabla_volumen_concreto.setHorizontalHeaderLabels(map(str, self.tabla_volumen_concreto_peso.columns))


        # Llenar la tabla con los datos del DataFrame
        for i, row in enumerate(self.tabla_volumen_concreto_peso.itertuples()):
            for j, value in enumerate(row[1:], start=0):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  # Establecer la alineación horizontal centrada de los elementos
                self.tabla_volumen_concreto.setItem(i, j, item)

        self.tabla_volumen_concreto.setVerticalHeaderLabels(self.tabla_volumen_concreto_peso.index)
             
        self.setStyleSheet(
            """
            QWidget {
                background-color: #f2f2f2;
                color: #333;
                font-size: 14px;
            }
            QLabel {
                font-weight: bold;
                margin-bottom: 5px;
            }
            QPushButton {
                padding: 8px;
                margin-bottom: 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
            }
            QPushButton#CantidadMateriales {
                 
                width: 300px; /* Establece un ancho máximo */
            }
            QPushButton#PesoUnitario {
                 
                min-width: 100px; /* Establece un ancho mínimo para el botón */
                max-width: 300px; /* Establece un ancho máximo para el botón */ /* Cambia el color del borde */
            }
            QPushButton#ProporcionVolumen {
                 
                min-width: 100px; /* Establece un ancho mínimo para el botón */
                max-width: 300px; /* Establece un ancho máximo para el botón */ /* Cambia el color del borde */
            }
            QPushButton#limpiarButton {
                background-color: #fe0000; /* Cambia el color de fondo */
                border-color: #d32f2f;
                min-width: 100px; /* Establece un ancho mínimo para el botón */
                max-width: 300px; /* Establece un ancho máximo para el botón */ /* Cambia el color del borde */
                
            }
            QMainWindow::title {
                background-color: #4CAF50;
                color: white;
                padding: 6px;
            }QTableWidget::item {
                 border: 2px solid #9c9c9c; border-radius: 5px;
            }
            """
        )

    def calcularResistencia(self):
        resistencia_diseño_str = self.resistencia_input.text()
        if resistencia_diseño_str:
            try:
                resistencia_diseño = float(resistencia_diseño_str)
                if resistencia_diseño < 210:
                    resistencia_requerida = resistencia_diseño + 70
                elif 210 <= resistencia_diseño <= 350:
                    resistencia_requerida = resistencia_diseño + 85
                else:
                    resistencia_requerida = resistencia_diseño + 100
                    
                self.resistencia_requerida_label.setText(f"{resistencia_requerida}")
            except ValueError:
                self.resistencia_requerida_label.setText("Necesita conocer la Resistencia de Diseño")
                
        else:
            self.resistencia_requerida_label.setText("Necesita conocer la Resistencia de Diseño")

    def calcularAireAtrapado(self):
    # Obtén el tamaño máximo nominal del agregado grueso de la tabla
        tamanio_nominal_item = self.tableWidget.item(2, 6)  # Fila 2 (agregado grueso), Columna 6 (tamaño máximo nominal)
        
        if tamanio_nominal_item:
            tamanio_nominal = tamanio_nominal_item.text()

            # Busca el valor en la tabla self.table_aire
            for i in range(self.table_aire.rowCount()):
                if self.table_aire.item(i, 0).text() == tamanio_nominal:
                    aire_atrapado = self.table_aire.item(i, 1).text()
                    # Muestra el valor de aire atrapado en algún widget de la interfaz, por ejemplo, en un QLabel
                    self.aire_atrapado_label.setText(f"{aire_atrapado}")
                    return

        # Si no se encuentra el valor o no hay un elemento seleccionado, muestra un mensaje de error
        self.aire_atrapado_label.setText("Necesita conocer el TMN del A.G")
  
    def calcularRelacionAguaCemento(self):
        resistencia_requerida_str = self.resistencia_requerida_label.text().split(":")[-1].strip()
        if resistencia_requerida_str:
            try:
                resistencia_requerida = float(resistencia_requerida_str)

                resistencias = []
                relaciones_agua_cemento_sin_aire = []
                relaciones_agua_cemento_con_aire = []

                for i in range(self.table_agua_cemento.rowCount()):
                    resistencias.append(float(self.table_agua_cemento.item(i, 0).text()))
                    relaciones_agua_cemento_sin_aire.append(float(self.table_agua_cemento.item(i, 1).text()))
                    relaciones_agua_cemento_con_aire.append(float(self.table_agua_cemento.item(i, 2).text()))

                if resistencia_requerida in resistencias:
                    indice = resistencias.index(resistencia_requerida)
                    relacion_sin_aire = relaciones_agua_cemento_sin_aire[indice]
                    relacion_con_aire = relaciones_agua_cemento_con_aire[indice]
                else:
                    idx = np.searchsorted(resistencias, resistencia_requerida)
                    x1, x2 = resistencias[idx - 1], resistencias[idx]
                    y1_sin_aire, y2_sin_aire = relaciones_agua_cemento_sin_aire[idx - 1], relaciones_agua_cemento_sin_aire[idx]
                    y1_con_aire, y2_con_aire = relaciones_agua_cemento_con_aire[idx - 1], relaciones_agua_cemento_con_aire[idx]

                    relacion_sin_aire = round((y1_sin_aire + ((y2_sin_aire - y1_sin_aire) / (x2 - x1)) * (resistencia_requerida - x1)), 3)
                    relacion_con_aire = round((y1_con_aire + ((y2_con_aire - y1_con_aire) / (x2 - x1)) * (resistencia_requerida - x1)), 3)

                # Verificar si los botones de radio están visibles antes de actualizar las etiquetas
                if self.radio_sin_aire.isVisible() and self.radio_con_aire.isVisible():
                    if self.radio_sin_aire.isChecked():
                        self.relacion_agua_cemento_sin_aire_label.setText(f"{relacion_sin_aire}")
                        self.relacion_agua_cemento_sin_aire_label.show()
                        self.relacion_agua_cemento_con_aire_label.setText(f"{relacion_con_aire}")
                        self.relacion_agua_cemento_con_aire_label.hide()
                    else:
                        self.relacion_agua_cemento_sin_aire_label.setText(f"{relacion_sin_aire}")
                        self.relacion_agua_cemento_sin_aire_label.hide() 
                        self.relacion_agua_cemento_con_aire_label.setText(f"{relacion_con_aire}")
                        self.relacion_agua_cemento_con_aire_label.show()

            except ValueError:
                self.relacion_agua_cemento_sin_aire_label.setText("Necesita conocer la Resistencia Requerida")

 
    def calcularVolumenAgua(self):

    # Obtener el valor de slump ingresado en la interfaz gráfica
        slump_value = self.slump_input.text()

        # Obtener el tamaño máximo nominal del agregado grueso seleccionado en la interfaz gráfica
        tamanio_nominal_item = self.tableWidget.item(2, 6)  # Fila 2 (agregado grueso), Columna 6 (tamaño máximo nominal)
        if tamanio_nominal_item:
            tamanio_nominal = tamanio_nominal_item.text()

            # Determinar qué tabla utilizar según el botón de radio seleccionado
            if self.radio_sin_aire.isChecked():
                tabla_agua = self.tabla_agua_concreto_sin_aire_incorporado
            else:
                tabla_agua = self.tabla_agua_concreto_con_aire_incorporado

            # Buscar el valor de slump en el índice correspondiente de la tabla
            if slump_value in tabla_agua.index:
                # Buscar el tamaño máximo nominal en la primera fila de la tabla
                if tamanio_nominal in tabla_agua.columns:
                    volumen_agua = tabla_agua.loc[slump_value, tamanio_nominal]
                    # Mostrar el volumen de agua en algún widget de la interfaz, por ejemplo, en un QLabel
                    self.volumen_agua_label.setText(f"{volumen_agua}")
                 
                    return
                     
        # Si no se encuentra el valor de slump o el tamaño máximo nominal, muestra un mensaje de error
        self.volumen_agua_label.setText("Necesita conocer el TMN del A.G y slump")

    # Calculo del volumen grueso seco y compactado por unidad de volumen de concreto para diversos valores de modulos de finura
    def calcularVolumenAgregadoGrueso(self):

    # Obtener el tamaño máximo nominal del agregado grueso seleccionado en la interfaz gráfica
        tamanio_nominal_item = self.tableWidget.item(2, 6)  # Fila 2 (agregado grueso), Columna 6 (tamaño máximo nominal)
        if tamanio_nominal_item:
            tamanio_nominal = tamanio_nominal_item.text()

            # Obtener el valor del módulo de finura del agregado fino ingresado en la interfaz gráfica
            modulo_finura_agregado_fino_item = self.tableWidget.item(1, 1)  # Fila 1 (agregado fino), Columna 1 (módulo de finura)
            if modulo_finura_agregado_fino_item:
                modulo_finura_agregado_fino = float(modulo_finura_agregado_fino_item.text())

                # Verificar si hay datos en el DataFrame
                if not self.tabla_volumen_concreto_peso.empty:

                    # Verificar si el tamaño nominal y el módulo de finura están presentes en el DataFrame
                    if tamanio_nominal in self.tabla_volumen_concreto_peso.index and modulo_finura_agregado_fino in self.tabla_volumen_concreto_peso.columns:
                        volumen_agregado_grueso = self.tabla_volumen_concreto_peso.loc[tamanio_nominal, modulo_finura_agregado_fino]

                        # Mostrar el volumen de agregado grueso en algún widget de la interfaz, por ejemplo, en un QLabel
                        self.volumen_agregado_grueso_label.setText(f"{volumen_agregado_grueso}")
                        return

                    else:

                        # Obtener los valores de módulo de finura más cercanos en la tabla
                        columnas = list(self.tabla_volumen_concreto_peso.columns)
                        lower_modulo = max(col for col in columnas if col <= modulo_finura_agregado_fino)
                        upper_modulo = min(col for col in columnas if col >= modulo_finura_agregado_fino)

                        # Obtener los valores de volumen correspondientes a los módulos de finura más cercanos
                        lower_value = self.tabla_volumen_concreto_peso.loc[tamanio_nominal, lower_modulo]
                        upper_value = self.tabla_volumen_concreto_peso.loc[tamanio_nominal, upper_modulo]

                        # Calcular el volumen interpolado utilizando la interpolación lineal
                        interpolated_value = lower_value + (upper_value - lower_value) * ((modulo_finura_agregado_fino - lower_modulo) / (upper_modulo - lower_modulo))

                        # Mostrar el volumen de agregado grueso interpolado en algún widget de la interfaz, por ejemplo, en un QLabel
                        self.volumen_agregado_grueso_label.setText(f"{interpolated_value}")
                        return

        # Si no se encuentra el valor del tamaño nominal o del módulo de finura, muestra un mensaje de error
        self.volumen_agregado_grueso_label.setText("Necesita conocer el TMN del A.G y el M.F del A.F")

    def calcularPesoCemento(self):

        # Obtener la relación agua-cemento
        relacion_agua_cemento_str = float(self.relacion_agua_cemento_sin_aire_label.text() if self.radio_sin_aire.isChecked() else self.relacion_agua_cemento_con_aire_label.text())

        # Obtener el volumen de agua
        volumen_agua_str = float(self.volumen_agua_label.text() if self.radio_sin_aire.isChecked() else self.volumen_agua_label.text())

        # Calculamos el peso del cemento
        if relacion_agua_cemento_str is not None and volumen_agua_str is not None:
            peso_cemento = round((volumen_agua_str/relacion_agua_cemento_str), 3)
            # Mostrar el peso del cemento en algún widget de la interfaz, por ejemplo, en un QLabel
            self.peso_cemento_label.setText(f"{peso_cemento}")
        else:
            # Si no se puede calcular el peso del cemento, mostrar un mensaje de error
            self.peso_cemento_label.setText("Necesita conocer la relacion a/c y volumen de agua")
  
    def calcularPesoAgregadoGrueso(self):
      
        # Obtener el peso seco compactado del agregado grueso desde la tabla
        peso_seco_compactado_item = self.tableWidget.item(2, 5)  # Fila 2 (agregado grueso), Columna 5 (peso seco compactado)
        if peso_seco_compactado_item:
            peso_seco_compactado = float(peso_seco_compactado_item.text())

            # Calcular el volumen del agregado grueso
            volumen_agregado_grueso_str = float(self.volumen_agregado_grueso_label.text())

            # Calcular el peso del agregado grueso
            if volumen_agregado_grueso_str is not None:
                peso_agregado_grueso = round(peso_seco_compactado * volumen_agregado_grueso_str, 3)

                # Mostrar el peso del agregado grueso en algún widget de la interfaz
                self.peso_agregado_grueso_label.setText(f"{peso_agregado_grueso}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.peso_agregado_grueso_label.setText("Necesita conocer el PUC del A.G y volumen del A.G")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.peso_agregado_grueso_label.setText("Necesita conocer el PUC del A.G y volumen del A.G")  

    # Calculamos el volumen Absoluto del Cemento
    def volumenCemento(self):
       
        peso_especifico_cemento_item = self.tableWidget.item(0, 0)  # Fila 0 (cemento), Columna 0 (peso especifico)
        if peso_especifico_cemento_item:
            peso_especifico_cemento = float(peso_especifico_cemento_item.text())

            # Calcular el peso del cemento
            peso_cemento_str = float(self.peso_cemento_label.text())

            # Calcular el volumen del cemento
            if peso_cemento_str is not None:
                volumen_cemento = round(peso_cemento_str/peso_especifico_cemento, 3)

                # Mostrar el volumen del cemento en algún widget de la interfaz
                self.volumen_cemento_label.setText(f"{volumen_cemento}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.volumen_cemento_label.setText("Necesita conocer el Contenido Cemento y su P.E")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.volumen_cemento_label.setText("Necesita conocer el Contenido Cemento y su P.E")   

    def volumenAguaAbsoluto(self):

        # Obtener el volumen de agua
        volumen_agua_str = float(self.volumen_agua_label.text() if self.radio_sin_aire.isChecked() else self.volumen_agua_label.text())

        # Calculamos el volumen de agua
        if  volumen_agua_str is not None:
            volumen_agua_str = round((volumen_agua_str/1000), 3)
            # Mostrar el peso del cemento en algún widget de la interfaz, por ejemplo, en un QLabel
            self.volumen_agua_absoluto_label.setText(f"{volumen_agua_str}")
        else:
            # Si no se puede calcular el peso del cemento, mostrar un mensaje de error
            self.volumen_agua_absoluto_label.setText("Necesita conocer el Volumen de Agua")

    def volumenAireAbsoluto(self):

        # Obtener el volumen de agua
        volumen_aire_str = float(self.aire_atrapado_label.text())

        # Calculamos el volumen de agua
        if  volumen_aire_str is not None:
            volumen_aire_str = round((volumen_aire_str/100), 3)
            # Mostrar el peso del cemento en algún widget de la interfaz, por ejemplo, en un QLabel
            self.volumen_aire_absoluto_label.setText(f"{volumen_aire_str}")
        else:
            # Si no se puede calcular el peso del cemento, mostrar un mensaje de error
            self.volumen_aire_absoluto_label.setText("Necesita conocer el Aire Atrapado")

    # Calculamos el volumen Absoluto del Agregado Grueso
    def volumenAgregadoGruesoAbsoluto(self):
      
        # Obtener el peso seco compactado del agregado grueso desde la tabla
        peso_especifico_agregado_grueso_item = self.tableWidget.item(2, 0)  # Fila 2 (agregado grueso), Columna 0 (peso especifico)
        if peso_especifico_agregado_grueso_item:
            peso_especifico_agregado_grueso = float(peso_especifico_agregado_grueso_item.text())

            # Calcular el peso del agregado grueso
            peso_agregado_grueso_str =  float(self.peso_agregado_grueso_label.text())
 
            # Calcular el volumen absoluto del agregado grueso
            if peso_agregado_grueso_str is not None:
                volumen_absoluto_agregado_grueso = round(peso_agregado_grueso_str/ peso_especifico_agregado_grueso, 3)

                # Mostrar el peso del agregado grueso en algún widget de la interfaz
                self.volumen_absoluto_agregado_grueso_label.setText(f"{volumen_absoluto_agregado_grueso}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.volumen_absoluto_agregado_grueso_label.setText("Necesita conocer el Peso de A.G y su P.E")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.volumen_absoluto_agregado_grueso_label.setText("Necesita conocer el Peso de A.G y su P.E")

    def volumenAgregadoFinoAbsoluto(self):
      
        # Obtener los valores de los volúmenes absolutos de los diferentes componentes
        volumen_agregado_grueso = float(self.volumen_absoluto_agregado_grueso_label.text())
        volumen_agua = float(self.volumen_agua_absoluto_label.text())
        volumen_aire = float(self.volumen_aire_absoluto_label.text())
        volumen_cemento = float(self.volumen_cemento_label.text())

        # Calcular el volumen de agregado fino
        volumen_agregado_fino = 1 - (volumen_agregado_grueso + volumen_agua + volumen_aire + volumen_cemento)

        # Mostrar el volumen de agregado fino en algún widget de la interfaz
        self.volumen_absoluto_agregado_fino_label.setText(f"{volumen_agregado_fino}")

    def calcularPesoAgregadoFino(self):
       
        # Obtener el peso especifico del agregado fino desde la tabla
        peso_especifico_fino_item = self.tableWidget.item(1, 0)  # Fila 1 (agregado fino), Columna 0 (peso especifico)
        if peso_especifico_fino_item:
            peso_especifico_fino = float(peso_especifico_fino_item.text())

            # Calcular el volumen del agregado fino
            volumen_agregado_fino_str = float(self.volumen_absoluto_agregado_fino_label.text())

            # Calcular el peso del agregado fino
            if volumen_agregado_fino_str is not None:
                peso_agregado_fino = round(peso_especifico_fino * volumen_agregado_fino_str, 3)

                # Mostrar el peso del agregado grueso en algún widget de la interfaz
                self.peso_agregado_fino_label.setText(f"{peso_agregado_fino}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.peso_agregado_fino_label.setText("Necesita conocer el Peso de A.F y su P.E")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.peso_agregado_fino_label.setText("Necesita conocer el Peso de A.F y su P.E")

    # Correccion por humedad de los agregados

    def agregadoGruesoCorr(self):
       
        # Obtener la humedad natural del agregado grueso desde la tabla
        humedad_agregado_grueso_item = self.tableWidget.item(2, 2)  # Fila 2 (agregado grueso), Columna 2 (humedad natural)
        if humedad_agregado_grueso_item:
            humedad_agregado_grueso = float(humedad_agregado_grueso_item.text())

            # Obteniendo el peso seco del agregado grueso
            peso_seco_agregado_grueso_str = float(self.peso_agregado_grueso_label.text())

            # Calcular el peso corregido por humedad del agregado grueso
            if peso_seco_agregado_grueso_str is not None:
                peso_agregado_grueso_corregido = round(peso_seco_agregado_grueso_str * ((humedad_agregado_grueso/100)+1), 3)

                # Mostrar el peso del agregado grueso en algún widget de la interfaz
                self.peso_agregado_grueso_corregido_label.setText(f"{peso_agregado_grueso_corregido}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.peso_agregado_grueso_corregido_label.setText("Necesita concer el Peso de A.G y su Humedad Natural")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.peso_agregado_grueso_corregido_label.setText("Necesita concer el Peso de A.G y su Humedad Natural")


    def agregadoFinoCorr(self):

        # Obtener la humedad natural del agregado grueso desde la tabla
        humedad_agregado_fino_item = self.tableWidget.item(1, 2)  # Fila 1 (agregado fino), Columna 2 (humedad natural)
        if humedad_agregado_fino_item:
            humedad_agregado_fino = float(humedad_agregado_fino_item.text())

            # Obteniendo el peso seco del agregado fino
            peso_seco_agregado_fino_str = float(self.peso_agregado_fino_label.text())

            # Calcular el peso corregido por humedad del agregado fino
            if peso_seco_agregado_fino_str is not None:
                peso_agregado_fino_corregido = round(peso_seco_agregado_fino_str * ((humedad_agregado_fino/100)+1), 3)

                # Mostrar el peso del agregado grueso en algún widget de la interfaz
                self.peso_agregado_fino_corregido_label.setText(f"{peso_agregado_fino_corregido}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.peso_agregado_fino_corregido_label.setText("Necesita concer el Peso de A.F y su Humedad Natural")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.peso_agregado_fino_corregido_label.setText("Necesita concer el Peso de A.F y su Humedad Natural")

    # Aporte de agua de los agregados
    
    def aporteagregadogrueso(self):

        humedad_agregado_grueso_item = self.tableWidget.item(2, 2)  # Fila 2 (agregado grueso), Columna 2 (humedad natural)
        porcentaje_absorcion_agregado_grueso_item = self.tableWidget.item(2, 3)  # Fila 2 (agregado grueso), Columna 3(Porcentaje de absorcion)
        if humedad_agregado_grueso_item and porcentaje_absorcion_agregado_grueso_item:
            humedad_agregado_grueso = float(humedad_agregado_grueso_item.text())
            porcentaje_absorcion_agregado_grueso = float( porcentaje_absorcion_agregado_grueso_item.text())

            # Obteniendo el peso seco del agregado grueso
            peso_seco_agregado_grueso_str = float(self.peso_agregado_grueso_label.text())

            # Calcular el aporte de agua del agregado grueso
            if peso_seco_agregado_grueso_str is not None:
                aporte_agregado_grueso = round(peso_seco_agregado_grueso_str * (humedad_agregado_grueso - porcentaje_absorcion_agregado_grueso)/100, 3)

                # Mostrar el aporte de agua del agregado grueso en algún widget de la interfaz
                self.aporte_agregado_grueso_label.setText(f"{aporte_agregado_grueso}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.aporte_agregado_grueso_label.setText("Necesita cono cer el Peso del A.G y su % Abs y Humedad")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.aporte_agregado_grueso_label.setText("Necesita cono cer el Peso del A.G y su % Abs y Humedad")

    def aporteagregadofino(self):        

        # Obtener la humedad natural del agregado grueso desde la tabla
        humedad_agregado_fino_item = self.tableWidget.item(1, 2)  # Fila 1 (agregado fino), Columna 2 (humedad natural)
        porcentaje_absorcion_agregado_fino_item = self.tableWidget.item(1, 3)  # Fila 1 (agregado fino), Columna 3  (porcentaje de absorcion)

        if humedad_agregado_fino_item and  porcentaje_absorcion_agregado_fino_item:
            humedad_agregado_fino = float(humedad_agregado_fino_item.text())
            porcentaje_absorcion_agregado_fino = float( porcentaje_absorcion_agregado_fino_item.text())

            # Obteniendo el peso seco del agregado fino
            peso_seco_agregado_fino_str = float(self.peso_agregado_fino_label.text())

            # Calcular el aporte de agua del agregado grueso
            if peso_seco_agregado_fino_str is not None:
                aporte_agregado_fino = round(peso_seco_agregado_fino_str * (humedad_agregado_fino - porcentaje_absorcion_agregado_fino)/100, 3)

                # Mostrar el aporte de agua del agregado grueso en algún widget de la interfaz
                self.aporte_agregado_fino_label.setText(f"{aporte_agregado_fino}")
            else:
                # Si no se puede calcular el peso del agregado grueso, mostrar un mensaje de error
                self.aporte_agregado_fino_label.setText("Necesita cono cer el Peso del A.F y su % Abs y Humedad")
        else:
            # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.aporte_agregado_fino_label.setText("Necesita cono cer el Peso del A.F y su % Abs y Humedad")

    # Cantidad de materiales corregidas por humedad
    def cantidadCemento(self):
       
      cantidad_cemento_str = float(self.peso_cemento_label.text())
      # Mostrar el aporte de agua del agregado grueso en algún widget de la interfaz
      self.cantidad_cemento_label.setText(f"{cantidad_cemento_str}")

    def cantidadAguaCorregido(self):
      
        # Obtenemos el volumen de agua sin corregir por humedad
        cantidad_agua_str = float(self.volumen_agua_label.text())

        # Obtenemos el aporte de agua del agregado grueso
        agua_agregado_grueso_str = float(self.aporte_agregado_grueso_label.text())
        
        # Obtenemos el aporte de agua del agregado fino
        agua_agregado_fino_str = float(self.aporte_agregado_fino_label.text())

        # Verificar si los valores son None y asignarles 0 si es así
        if agua_agregado_grueso_str is None:
            agua_agregado_grueso_str = 0.0
        if agua_agregado_fino_str is None:
            agua_agregado_fino_str = 0.0

        # Calcular la cantidad de agua corregida por aporte de agregado
        cantidad_agua_corregida = round((cantidad_agua_str - (agua_agregado_grueso_str + agua_agregado_fino_str)), 3)
        
        # Mostrar el aporte de agua corregida en algún widget de la interfaz
        self.cantidad_agua_label.setText(f"{cantidad_agua_corregida}")

    def cantidadAgregadoGrueso(self):
       
      cantidad_agregado_grueso_str = float(self.peso_agregado_grueso_corregido_label.text())
        # Mostrar el aporte de agua del agregado grueso en algún widget de la interfaz
      self.cantidad_agregado_grueso_label.setText(f"{cantidad_agregado_grueso_str}")

    def cantidadAgregadoFino(self):
       
      cantidad_agregado_fino_str = float(self.peso_agregado_fino_corregido_label.text())
      # Mostrar el aporte de agua del agregado grueso en algún widget de la interfaz
      self.cantidad_agregado_fino_label.setText(f"{cantidad_agregado_fino_str}")

    def mostrarResultados(self):
         
        # Llamar a cada una de las funciones para obtener los resultados
        self.cantidadCemento()
        self.cantidadAguaCorregido()
        self.cantidadAgregadoGrueso()
        self.cantidadAgregadoFino()

        # Obtener los textos de las etiquetas actualizadas
        texto_cemento = self.cantidad_cemento_label.text()
        texto_agua = self.cantidad_agua_label.text()
        texto_agregado_grueso = self.cantidad_agregado_grueso_label.text()
        texto_agregado_fino = self.cantidad_agregado_fino_label.text()

        # Crear el DataFrame con los resultados
        df = pd.DataFrame({
            'Cemento (kg/m3)': [texto_cemento],
            'Agua Corregida (lt/m3)': [texto_agua],
            'Agregado Grueso (kg/m3)': [texto_agregado_grueso],
            'Agregado Fino (kg/m3)': [texto_agregado_fino]
        })

        # Convertir el DataFrame a HTML
        html_table = df.to_html(index=False, classes='dataframe', escape=False)

        # Agregar atributo style a cada celda de la tabla para centrar horizontalmente el texto
        html_table = html_table.replace('<td>', '<td style="text-align:center; font-weight: bold ; background-color: yellow; color: red; border: 1px solid blue;">')

        # Envolver la tabla en un div para centrar horizontalmente
        html_table = '<div style="text-align:center; border-radius: 10px; width: 550px; height: 300px;">' + html_table + '</div>'

        # Mostrar el HTML en el QLabel
        self.mostrar_resultado_label.setText(html_table)

    # Calculamos el Peso Unitario de Obra o Porporcion en Peso (W.U.O)
        
    def pesoUnitarioCemento(self):
       
      cantidad_cemento_str = float(self.peso_cemento_label.text())
      cantidad_cemento_unitario = round((cantidad_cemento_str/cantidad_cemento_str), 2)
      #Agregando los calculos a la etiqueta
      self.cantidad_cemento_unitario_label.setText(f"{cantidad_cemento_unitario}")

    def pesoUnitarioAgua(self):
         
        # Obtener las cantidades

        cantidad_cemento_str = float(self.peso_cemento_label.text())
        cantidad_agua_str  = float(self.cantidad_agua_label.text())
        #Calculando cantidad unitaria de agua
        cantidad_agua_unitario = round((cantidad_agua_str/cantidad_cemento_str), 2)

        #Agregando los calculos a la etiqueta
        self.cantidad_agua_unitario_label.setText(f"{cantidad_agua_unitario}")

    def pesoUnitarioAgregadoGrueso(self):
        
        # Obtener las cantidades

        cantidad_cemento_str = float(self.peso_cemento_label.text())
        cantidad_agregado_grueso_str  = float(self.cantidad_agregado_grueso_label.text())
        #Calculando cantidad unitaria de agua
        cantidad_agregado_grueso_unitario = round((cantidad_agregado_grueso_str/cantidad_cemento_str), 2)

        #Agregando los calculos a la etiqueta
        self.cantidad_agregado_grueso_unitario_label.setText(f"{cantidad_agregado_grueso_unitario}")

    def pesoUnitarioAgregadoFino(self):
        
        # Obtener las cantidades

        cantidad_cemento_str = float(self.peso_cemento_label.text())
        cantidad_agregado_fino_str  = float(self.cantidad_agregado_fino_label.text())
        #Calculando cantidad unitaria de agua
        cantidad_agregado_fino_unitario = round((cantidad_agregado_fino_str/cantidad_cemento_str), 2)

        #Agregando los calculos a la etiqueta
        self.cantidad_agregado_fino_unitario_label.setText(f"{cantidad_agregado_fino_unitario}")

    def mostrarPesosUnitarios(self):
         
        # Llamar a cada una de las funciones para obtener los resultados
        self.pesoUnitarioCemento()
        self.pesoUnitarioAgua()
        self.pesoUnitarioAgregadoGrueso()
        self.pesoUnitarioAgregadoFino()

        # Obtener los textos de las etiquetas actualizadas
        texto_cemento_unitario = self.cantidad_cemento_unitario_label.text()
        texto_agua_unitario = self.cantidad_agua_unitario_label.text()
        texto_agregado_grueso_unitario = self.cantidad_agregado_grueso_unitario_label.text()
        texto_agregado_fino_unitario = self.cantidad_agregado_fino_unitario_label.text()

        # Crear el DataFrame con los resultados
        df1 = pd.DataFrame({
            'Cemento': [texto_cemento_unitario],
            'Agua': [texto_agua_unitario],
            'Agregado Grueso': [texto_agregado_grueso_unitario],
            'Agregado Fino': [texto_agregado_fino_unitario]
        })

        # Convertir el DataFrame a HTML
        html_table = df1.to_html(index=False, classes='dataframe', escape=False)

        # Agregar atributo style a cada celda de la tabla para centrar horizontalmente el texto
        html_table = html_table.replace('<td>', '<td style="text-align:center; font-weight: bold ; background-color: yellow; color: red; border: 1px solid blue;">')

        # Envolver la tabla en un div para centrar horizontalmente
        html_table = '<div style="text-align:center; border-radius: 10px; width: 800px; height: 300px;">' + html_table + '</div>'

        # Mostrar el HTML en el QLabel
        self.peso_obra_unitario_label.setText(html_table)

    # Calculamos el Volumen aparente o proporcion en volumen en pies cubicos
        
    def proporcionVolumenCemento(self):
       
      cantidad_cemento_str = float(self.peso_cemento_label.text())
      proporcion_volumen_cemento= round((cantidad_cemento_str/cantidad_cemento_str), 2)
      #Agregando los calculos a la etiqueta
      self.proporcion_volumen_cemento_label.setText(f"{proporcion_volumen_cemento}")

    def proporcionVolumenAgua(self):
         
        # Obtener las cantidades unitarias de agua
        cantidad_agua_str  = float(self.cantidad_agua_unitario_label.text())
        #Calculando cantidad unitaria de agua
        proporcion_volumen_agua = round((cantidad_agua_str*42.5), 2)

        #Agregando los calculos a la etiqueta
        self.porporcion_volumen_agua_label.setText(f"{proporcion_volumen_agua}")

    def proporcionVolumenAgregadoGrueso(self):
         
        # Obtener las cantidades Peso Unitario del Agregado Grueso y su Peso Unitario Suelto
        peso_unitario_suelto_agregado_grueso_item = self.tableWidget.item(2, 4)  # Fila 2 (agregado grueso), Columna 4 (peso unitario suelto)
        humedad_natural_agregado_grueso_item = self.tableWidget.item(2, 2)  # Fila 2 (agregado grueso), Columna 2  (humedad natural)

        if peso_unitario_suelto_agregado_grueso_item and  humedad_natural_agregado_grueso_item:
            peso_unitario_suelto_agregado_grueso = float(peso_unitario_suelto_agregado_grueso_item.text())
            humedad_natural_agregado_grueso = float(humedad_natural_agregado_grueso_item.text())
        
            #Obteniendo el Peso Unitario del Agregado Grueso
            cantidad_agregado_grueso_unitario  = float(self.cantidad_agregado_grueso_unitario_label.text())

            #Calculando la proporcion de volumen de agregado grueso
            if  cantidad_agregado_grueso_unitario is not None:
                
                proporcion_volumen_agregado_grueso= round((cantidad_agregado_grueso_unitario *42.5*35.31/(peso_unitario_suelto_agregado_grueso*(1 + humedad_natural_agregado_grueso/100))), 2)

                 # Mostrar la proporcion de volumen de agregado grueso en algún widget de la interfaz
                self.proporcion_volumen_agregado_grueso_label.setText(f"{proporcion_volumen_agregado_grueso}")
        
            else:
                # Si no se puede calcular la proporcion en volumen de agregado grueso, mostrar un mensaje de error
                self.proporcion_volumen_agregado_grueso_label.setText("Necesita conocer la humedad antural y peso unitario suelto del A.G")
        else:
             # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.proporcion_volumen_agregado_grueso_label.setText("Necesita conocer la humedad antural y peso unitario suelto del A.G")

    def proporcionVolumenAgregadoFino(self):
         
        # Obtener las cantidades Peso Unitario del Agregado Fino y su Peso Unitario Suelto
        peso_unitario_suelto_agregado_fino_item = self.tableWidget.item(1, 4)  # Fila 1 (agregado fino), Columna 4 (peso unitario suelto)
        humedad_natural_agregado_fino_item = self.tableWidget.item(1, 2)  # Fila 1 (agregado fino), Columna 2  (humedad natural)


        if peso_unitario_suelto_agregado_fino_item and  humedad_natural_agregado_fino_item:
            peso_unitario_suelto_agregado_fino = float(peso_unitario_suelto_agregado_fino_item.text())
            humedad_natural_agregado_fino = float(humedad_natural_agregado_fino_item.text())
        
            #Obteniendo el Peso Unitario del Agregado Fino
            cantidad_agregado_fino_unitario  = float(self.cantidad_agregado_fino_unitario_label.text())

            #Calculando la proporcion de volumen de agregado grueso
            if  cantidad_agregado_fino_unitario is not None:
                
                proporcion_volumen_agregado_fino= round((cantidad_agregado_fino_unitario *42.5*35.31/(peso_unitario_suelto_agregado_fino*(1 + humedad_natural_agregado_fino/100))), 2)

                 # Mostrar la proporcion de volumen de agregado grueso en algún widget de la interfaz
                self.proporcion_volumen_agregado_fino_label.setText(f"{proporcion_volumen_agregado_fino}")
        
            else:
                # Si no se puede calcular la proporcion en volumen de agregado grueso, mostrar un mensaje de error
                self.proporcion_volumen_agregado_fino_label.setText("Necesita conocer la humedad antural y peso unitario suelto del A.F")
        else:
             # Si no se encuentra el valor del peso seco compactado, mostrar un mensaje de error
            self.proporcion_volumen_agregado_fino_label.setText("Necesita conocer la humedad antural y peso unitario suelto del A.F")
  
    def mostrarProporcionVolumen(self):
         
        # Llamar a cada una de las funciones para obtener los resultados
        self.proporcionVolumenCemento()
        self.proporcionVolumenAgua()
        self.proporcionVolumenAgregadoGrueso()
        self.proporcionVolumenAgregadoFino()

        # Obtener los textos de las etiquetas actualizadas
        texto_cemento_proporcion_volumen = self.proporcion_volumen_cemento_label.text()
        texto_agua_proporcion_volumen = self.porporcion_volumen_agua_label.text()
        texto_agregado_grueso_proporcion_volumen = self.proporcion_volumen_agregado_grueso_label.text()
        texto_agregado_fino_proporcion_volumen = self.proporcion_volumen_agregado_fino_label.text()

        # Crear el DataFrame con los resultados
        df2 = pd.DataFrame({
            'Cemento': [texto_cemento_proporcion_volumen],
            'Agua': [texto_agua_proporcion_volumen],
            'Agregado Grueso': [texto_agregado_grueso_proporcion_volumen],
            'Agregado Fino': [texto_agregado_fino_proporcion_volumen]
        })

        # Convertir el DataFrame a HTML
        html_table = df2.to_html(index=False, classes='dataframe', escape=False)

        # Agregar atributo style a cada celda de la tabla para centrar horizontalmente el texto
        html_table = html_table.replace('<td>', '<td style="text-align:center; font-weight: bold ; background-color: yellow; color: red; border: 1px solid blue;">')

        # Envolver la tabla en un div para centrar horizontalmente
        html_table = '<div style="text-align:center; border-radius: 10px; width: 800px; height: 300px;">' + html_table + '</div>'

        # Mostrar el HTML en el QLabel
        self.proporcion_volumen_label.setText(html_table)

    def limpiarInterfaz(self):
       
    # Limpiar valores en widgets de peso específico
        self.tableWidget.clearContents()
        
        # Volver a establecer la alineación de texto en las celdas luego de limpiar los datos, es decir los datos que ingresemos a la tabla seguiran centrados horizontalmente.
        for i in range(3):
            for j in range(7):
                item = QTableWidgetItem("")
                item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
                self.tableWidget.setItem(i, j, item)
        
        self.resistencia_input.setText("")
        self.slump_input.setText("")
        self.relacion_agua_cemento_sin_aire_label.setText("")
        self.relacion_agua_cemento_con_aire_label.setText("")
        self.resistencia_requerida_label.setText("")
        self.peso_cemento_label.setText("")
        self.volumen_cemento_label.setText("")
        self.volumen_agua_label.setText("")
        self.volumen_agregado_grueso_label.setText("")
        self.volumen_absoluto_agregado_fino_label.setText("")
        self.volumen_agua_absoluto_label.setText("")
        self.peso_agregado_fino_label.setText("")
        self.aire_atrapado_label.setText("")
        self.volumen_aire_absoluto_label.setText("")
        self.peso_agregado_grueso_label.setText("")
        self.volumen_absoluto_agregado_grueso_label.setText("")
        self.peso_agregado_grueso_corregido_label.setText("")
        self.peso_agregado_fino_corregido_label.setText("")
        self.aporte_agregado_grueso_label.setText("")
        self.aporte_agregado_fino_label.setText("")
        self.mostrar_resultado_label.setText("")
        self.peso_obra_unitario_label.setText("")
        self.proporcion_volumen_label.setText("")

         # Desactivar los botones de radio
        self.desactivar_botones_radio()

    def desactivar_botones_radio(self):

        # Desactivar ambos botones de radio
        self.radio_sin_aire.setChecked(False)
        self.radio_con_aire.setChecked(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())