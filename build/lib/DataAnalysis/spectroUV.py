# ANALIZADOR ESPECTRO UV V.1.2.4
# Programa para graficar los datos del Espectro UV/Vis
# a partir de los archivos .ascii
# Author: F. Javier Morales M.
# Date: 08/11/2021

# MODO DE EMPLEO
# Utilizar en el editor Atom con el paquete Hydrogen
# o en la linea de comandos con:
# >  ---WORK IN PRGESS!---

# CHANGELOG:
# 22/11/2021 - Creado el archivo como funciones para importar
# 25/11/2021 - Creada la clase spectroUV, módulos data_filter,data_plotter, save_plot
# 25/11/2021 - Corregido el index del DataFrame
# 26/11/2021 - Corregidas las funciones de area_plotter() y save_plot()

# TODO:
# [X] Crear función con parámetros de nombre de archivo
# [X] Pasar parametro de carpeta y filtro de archivos
# [X] Agregar dentro de la función los comandos para generar gráfico
# [X] Guardar gráfico en PDF
# [X] Importar funciones con import data_analysis
# [X] Crear una clase para generar objetos
# [X] Generar un archivo .csv
# [X] Crear librería/paquete y módulos
# [X] Agregar argumentos de funciones default
# [X] Agregar argumentos opcionales
# [] Subir paquete a Pypip



import pandas as pd
import numpy as np
from numpy import trapz
# from scipy.integrate import simps
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from IPython.display import display, Latex, Math
from os import listdir
import natsort as nsrt
import DataAnalysis.helpers

# Mod 1.2.4
class spectroUV:


    def __init__(self):
        self.data = dict()
        self.title = 'Cinética'
        self.index = 'Wavelenght'
        self.x0 = 200
        self.xf = 300
        self.y0 = -0.05
        self.yf = 5.0
        self.c0 = 1
        self.cf = 15
        self.width = 23
        self.height = 15
        self.dx=1.0
        self.folder = 'CS1M150mLFiltrados'
        self.filter = 'CS1F-Dex'
        # self.area_params = {'dx' : 1.0}


    def data_filter(self, folder, filter):
        self.folder = folder
        self.filter = filter
        self.filtered_files = list()
        files = nsrt.natsorted(listdir(self.folder))
        for i in files:
            if self.filter in i:
                self.filtered_files.append(i)

        self.data = {}
        self.data = {'Wavelenght': list(range(700, 199, -1))}

        self.filtered_files = [s.split('.') for s in self.filtered_files]
        ext = self.filtered_files[0][1]
        self.filtered_files = [s.pop(0) for s in self.filtered_files]

        for file_name in self.filtered_files:
            abscol = list()
            with open(self.folder + '/' + file_name + '.' + ext, 'rb') as file:
                self.data.update({file_name: []})
                for i in range(88):
                    file.readline()

                for line in file:
                    columns = line.strip().split()
                    abscol.append(float(columns[1]))

                abs_array = np.array(abscol)
                self.data[file_name] = abs_array
                abscol = []
        # return self.data
        self.data_frame = pd.DataFrame(self.data)
        self.spectro_plotter(visible=False)
        self.area_plotter(visible=False)


    def spectro_plotter(self, title='Cinética', index='Wavelenght', x0=200, xf=300, y0=-0.05, yf=5.0, c0=1, cf=15, width=23, height=15, visible=True):
        self.title = title
        self.index = index
        if self.index == 'Wavelenght':
            self.data_frame.index = self.data[self.index]
        elif self.index == None:
            self.data_frame.index = self.data_frame.index
        else:
            self.data_frame.index = self.index

        self.x0 = x0
        self.xf = xf
        self.y0 = y0
        self.yf = yf
        self.c0 = c0
        self.cf = cf
        self.width = cm2in(width)
        self.height = cm2in(height)

        self.frame = self.data_frame.iloc[700-self.xf:,self.c0:self.cf+1]
        self.figure = self.data_frame.plot(x=self.data_frame.columns[0], y=self.data_frame.columns[self.c0:self.cf+1], legend=True, figsize=(self.width, self.height))
        self.figure.set_title(self.title, fontsize=14)
        self.figure.set_xlim(self.x0, self.xf)
        self.figure.set_ylim(self.y0, self.yf)
        self.figure.set_xlabel('Longitud de onda (nm)', fontsize=14)
        self.figure.set_ylabel('Abs', fontsize=14)
        # self.figure.set_visible(visible)
        self.figure = self.figure.get_figure()
        plt.grid()
        # plt.show()
        if visible == False:
            plt.close(self.figure)

        self.area_plotter(visible=False)
        # return self.figure, self.x0, self.xf, self.title, self.frame



    def area_plotter(self, dx=1.0,   visible=True):
        self.dx = dx
        def cm2in(value):
            return value/2.54

        area = list()

        for key in self.frame:
            area_trapz = trapz(y=self.frame[key], dx=self.dx)
            area.append(area_trapz)

        self.area_x = np.array(range(len(area))).reshape(-1,1)
        self.area_y = np.array(area)
        reg_line = LinearRegression()
        reg_line.fit(self.area_x.reshape(-1,1), self.area_y)
        self.Y_pred = reg_line.predict(self.area_x)
        # beta*x + alfa
        self.alfa = reg_line.intercept_
        self.beta = reg_line.coef_
        self.r_sq = reg_line.score(self.area_x, self.area_y)

        # plt.rcParams['text.usetex'] = True
        eq = '$y = {0:.2f}x + {1:.2f}$\n $R^2 = {2:.4f}$'.format(float(self.beta),self.alfa,self.r_sq)
        eq_latex = r'$$y = {0:.2f}x + {1:.2f}$$ $$R^2 = {2:.4f}$$'.format(float(self.beta),self.alfa,self.r_sq)
        self.reg_equation = Latex(eq_latex)
        self.figure_area = plt.figure(figsize=(cm2in(self.width), cm2in(self.height)))
        plt.plot(self.area_x, self.area_y, label='Area', marker='^', linestyle='dashed')
        plt.plot(self.area_x, self.Y_pred, color='red', label='y')
        # plt.gcf().set_size_inches(10,5) # otra opción para el tamaño de gráfico
        plt.suptitle(self.title, fontsize=14)
        plt.title('Area bajo la curva ({0} - {1} nm)'.format(self.x0, self.xf), fontsize=12)
        # plt.subtitle(subtitle)
        plt.ylabel('Area', fontsize=14)
        plt.xlabel('Tiempo(12h)', fontsize=14)
        plt.text(int(max(self.area_x)/2), max(self.area_y)-15, eq, fontsize=12)
        plt.grid()
        plt.legend()
        # self.figure_area.set_visible(visible)
        # plt.xlim(range(len(area)))
        # plt.ylim(-0.05,5.0)
        # plt.show()
        if visible == False:
            plt.close()

        # return self.figure_area, self.reg_equation


    @property
    def help(self):
        # self.data_plotter()
        # self.area_plotter()
        params = {'title': '\''+self.title+'\''+'   -> Titulo de los gráficos',
                'index' : '\''+self.index+'\''+'o None   -> Etiqueta de indinces de la tabla de datos',
                'x0' : str(self.x0)+'   -> Valor inicial de x para graficar',
                'xf' : str(self.xf)+'   -> Vaor final de x para graficar',
                'y0' : str(self.y0)+'   -> Valor inicial de y para graficar',
                'yf' : str(self.yf)+'   -> Valor final de y para graficar',
                'c0' : str(self.c0)+'   -> Columna inicial para graficar',
                'cf' : str(self.cf)+'   -> Columna final para graficar',
                'width' : str(self.width)+'   -> Ancho del gráfico en cm',
                'height' : str(self.height)+'   -> Alto del gráfico en cm'}
        params_area= {'dx' : str(self.dx)+'   -> Desplazamiento en x para el cálculo de areas'}
        print("""
INSTRUCCIONES DE USO:

    Creación del objeto spectroUV():
        Para crear el objeto asignamos a una variable dicho objeto:

        var = spectroUV()

        Una vez creado el objeto podemos cargar los archivos a analizar con
        la función data_filter(), la cual acepta dos parámetros:

        var.data_filter(\'<Nombre_de_carpeta>\', \'<filtro_de_archivos>\')

        Ejemplo:

        var.data_filter(\'{}\', \'{}\')\n""".format(self.folder, self.filter))

        print("""

    Propiedades:
    Con lo anterior ya podemos utilizar las siguientes propiedades y  funciones:

        var.help -> Muestra esta ayuda

        var.frame -> Muestra la tabla de datos creada con los parámetros por default

        var.figure -> Muestra el gráfico por default del espectro UV

        var.figure_area -> Muestra el gráfico por default de las areas bajo la curva

        var.reg_equation -> Muestra la ecuación lineal del gráfico de areas

        var.alfa -> Devuelve el valor de la ordenada al origen de bx + a

        var.beta -> Devuelve el valor de la pendiente de bx + a

    Funciones:
    Las siguitenes funciones aceptan parámetros, separados por coma, para cambiar los
    de default:

        spectro_plotter(): Genera gráfico del espectro

        var.spectro_plotter(<parámetro1>=<valor1> , <parámetro2>=<valor2>...)

        Parámetros por default:
        """)
        for key, value in params.items():
            print('\t \t {}={}'.format(key, value))

        print("""
        area_plotter(): Genera gráfico de areas

        var.area_plotter(<parámetro1>=<valor1> , <parámetro2>=<valor2>...)

        Parámetros por default:
        """)
        for key, value in params_area.items():
            print('\t \t {}={}'.format(key, value))

        print("""
        save_plot(): Guarda la figura actual en formato .PDF o el formato de elección
         (jpg, png, svg)

        var.save_plot(<var.figure> o <var.figure_area>, 'nombre_de_figura.pdf')

        save_data(): Guarda el frame actual en formato .CSV

        var.save_data('<nombre_de_archivo.csv>')
        """)
