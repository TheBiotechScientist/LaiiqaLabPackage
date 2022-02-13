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
from DataAnalysis.helpers import *

# Mod 1.2.4
class SpectroUV:

    # def data_filter(self, filter):
    #     filtered_files = list()
    #     files = nsrt.natsorted(listdir())
    #     for i in files:
    #         if filter in i:
    #             filtered_files.append(i)
    #
    #     data = dict()
    #     data = {'Wavelenght': list(range(700, 199, -1))}
    #
    #     filtered_files = [s.split('.') for s in filtered_files]
    #     ext = filtered_files[0][1]
    #     filtered_files = [s.pop(0) for s in filtered_files]
    #
    #     for file_name in filtered_files:
    #         abscol = list()
    #         with open(file_name + '.' + ext, 'rb') as file:
    #             data.update({file_name: []})
    #             for i in range(88):
    #                 file.readline()
    #
    #             for line in file:
    #                 columns = line.strip().split()
    #                 abscol.append(float(columns[1]))
    #
    #             abs_array = np.array(abscol)
    #             data[file_name] = abs_array
    #             abscol = []
    #     # return data
    #     self.frameall = pd.DataFrame(data)
    #     self.spectro_plotter(visible=False)
    #     self.area_plotter(visible=False)


    def plot(self, filter='Filter', title='Espectro UV', subtitle=None, index='Wavelength', xlabel='Longitud de onda (nm)', ylabel='Absorbancia', x0=200, xf=None, y0=-0.05, yf=5.0, c0=0, cf=None, width=23, height=15, grid=True, visible=True):
        w = cm2in(width)
        h = cm2in(height)
        self.c0 = c0
        self.x0 = x0
        self.xf = xf
        filtered_files = list()
        files = nsrt.natsorted(listdir())
        for i in files:
            if filter in i:
                filtered_files.append(i)

        data = dict()
        data = {index: []}

        ext = filtered_files[0].rsplit('.', 1)[1]
        filtered_files = [s.rsplit('.', 1) for s in filtered_files]
        filtered_files = [s.pop(0) for s in filtered_files]
        # print(filtered_files)
        # print(ext)

        for file_name in filtered_files:
            wave = list()
            abscol = list()
            with open(file_name + '.' + ext, 'r') as file:
                data.update({file_name: []})
                for i in range(88):
                    file.readline()

                for line in file:
                    columns = line.strip().split()
                    wave.append(int(float(columns[0])))
                    abscol.append(float(columns[1]))

                wave_array = np.array(wave)
                abs_array = np.array(abscol)
                data[file_name] = abs_array
                data[index] = wave_array
                wave = []
                abscol = []
        # return data
        self.frameall = pd.DataFrame(data)
        # self.plot(visible=False)
        # self.area_plotter(visible=False)


        if index == 'Wavelength':
            self.frameall.index = data[index]
        elif index == None:
            self.frameall.index = self.frameall.index
        else:
            self.frameall.index = index


        if self.xf == None:
            self.xf = max(self.frameall.index)
        else:
            self.xf = self.xf

        if cf == None:
            cf = len(self.frameall.columns)
        else:
            cf = cf

        self.frame = self.frameall.iloc[max(self.frameall.index)-self.xf:max(self.frameall.index)+1-self.x0,self.c0:cf+1]
        fig = self.frame.plot(y=self.frame.columns[self.c0+1:cf+1], legend=True, figsize=(w, h), grid=grid)
        plt.suptitle(title, fontsize=14)
        fig.set_title(subtitle, fontsize=12)
        fig.set_xlim(self.x0, self.xf)
        fig.set_ylim(y0, yf)
        fig.set_xlabel(xlabel, fontsize=14)
        fig.set_ylabel(ylabel, fontsize=14)
        # plt.grid()
        self.figure = fig.get_figure()
        if visible == False:
            plt.close()
        else:
            plt.show()


    def plot_area(self, title='Espectro UV', subtitle='Area bajo la curva', xlabel='Tiempo (h)', ylabel='Area', labelx='Area', labely='y', width=23, height=15, dx=1.0, visible=True):
        w = cm2in(width)
        h = cm2in(height)

        if subtitle == 'Area bajo la curva':
            subtitle = f'Area bajo la curva ({self.x0} - {self.xf} nm)'
        else:
            subtitle = subtitle

        area = list()

        for i in range(self.c0+1,len(self.frame.columns)):
            area_trapz = trapz(y=self.frame.iloc[:,i], dx=dx)
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
        self.reg_equation = '$y = {0:.2f}x + {1:.2f}$\n $R^2 = {2:.4f}$'.format(float(self.beta),self.alfa,self.r_sq)
        self.reg_equation_latex = Latex(self.reg_equation)

        area_plot = plt.figure(figsize=(w, h))
        plt.plot(self.area_x, self.area_y, label=labelx, marker='^', linestyle='dashed')
        plt.plot(self.area_x, self.Y_pred, color='red', label=labely)
        # plt.gcf().set_size_inches(10,5) # otra opción para el tamaño de gráfico
        plt.suptitle(title, fontsize=14)
        plt.title(subtitle, fontsize=12)
        # plt.subtitle(subtitle)
        plt.xlabel(xlabel, fontsize=14)
        plt.ylabel(ylabel, fontsize=14)
        plt.text(int(max(self.area_x)/2), max(self.area_y)-max(self.area_y)*0.15, self.reg_equation, fontsize=12)
        plt.grid()
        plt.legend()
        # fig_area.set_visible(visible)
        # plt.xlim(range(len(area)))
        # plt.ylim(-0.05,5.0)
        # plt.show()
        self.figure_area = area_plot.get_figure()
        if visible == False:
            plt.close()
        else:
            plt.show()

        # self.area_plot = fig_area.gcf()
        # return fig_area, self.reg_equation

    @property
    def help(self):
        # self.data_plotter()
        # self.area_plotter()
        params = {'filter': '\'Filter\'   -> Filtro del nombre de archivos a cargar',
                'title': '\'Cinética\'   -> Titulo del gráfico',
                'subtitle': 'None   -> Subtitulo del gráfico',
                'index' : '\'Wavelength\' || None   -> Etiqueta de indinces de la tabla de datos',
                'xlabel': '\'Longitud de onda (nm)\'   -> Etiqueta del eje x',
                'ylabel': '\'Abosorbancia\'   -> Etiqueta del eje y',
                'x0' : '200   -> Valor inicial de x para graficar',
                'xf' : 'None   -> Vaor final de x para graficar',
                'y0' : '-0.05   -> Valor inicial de y para graficar',
                'yf' : '0.5   -> Valor final de y para graficar',
                'c0' : '0   -> Columna inicial para graficar',
                'cf' : 'None   -> Columna final para graficar',
                'width' : '23   -> Ancho del gráfico en cm',
                'height' : '15   -> Alto del gráfico en cm',
                'visible': 'True || False  -> Mostrar o no el gráfico '}
        params_area= {'title' : '\'Cinética\'   -> Titulo del gráfico de areas',
                      'subtitle' : '\'Area bajo la curva\'   -> Subtitulo del gráfico de areas',
                      'xlabel' : '\'Tiempo (h)\'   -> Eiqueta del eje x',
                      'ylabel' : '\'Area\'   -> Eiqueta del eje y',
                      'dx' : '1.5   -> Desplazamiento en x para el cálculo de areas',
                      'labelx' : '\'Area\'   -> Leyenda de los puntos de area',
                      'labely' : '\'y\'   -> Leyenda de la linea de regresión lineal',
                      'width' : '23   -> Ancho del gráfico de areas',
                      'height' : '15   -> Alto del gráfico de areas',
                      'dx' : '1.0   -> Paso de integración para el cálculo de areas',
                      'visible' : 'True   -> Mostrar o no el gráfico de areas'}
        print("""

INSTRUCCIONES DE USO:

    Creación del objeto spectroUV():
        Para crear el objeto asignamos a una variable dicho objeto:

        obj = SpectroUV()

        Una vez creado el objeto podemos cargar y graficar los archivos a analizar con
        la función plot(), la cual acepta un parámetro obligatorio:

        obj.plot(\'<filtro_de_archivos_a_graficar>\')

        Ejemplo:

        obj.plot('2021_01_')   -> Graficará todos los archivos en carpeta que empiecen con la cadena de caracteres '2021_01_'.

        \n""")

        print("""

    Propiedades:
    Con lo anterior ya podemos utilizar las siguientes propiedades y funciones:

        obj.help -> Muestra esta ayuda

        obj.frameall -> Muestra la tabla de datos completos creada

        obj.frame -> Mestra la tabla de datos creada con los parámetros x0, xf

        obj.figure -> Muestra el gráfico por default del espectro UV

        obj.figure_area -> Muestra el gráfico por default de las areas bajo la curva

        obj.reg_equation -> Muestra la ecuación de regreseión lineal del gráfico de areas

        obj.alfa -> Devuelve el valor de la ordenada al origen de bx + a

        obj.beta -> Devuelve el valor de la pendiente de bx + a

    Funciones:
    Las siguitenes funciones aceptan parámetros, separados por coma, para cambiar los
    de default:

        plot(): Genera gráfico del espectro

        obj.plot(<parámetro1>=<valor1> , <parámetro2>=<valor2>...)


        Parámetros por default:
        """)
        for key, value in params.items():
            print('\t \t {}={}'.format(key, value))

        print("""

        plot_area(): Genera gráfico de areas

        obj.plot_area(<parámetro1>=<valor1> , <parámetro2>=<valor2>...)


        Parámetros por default:
        """)
        for key, value in params_area.items():
            print('\t \t {}={}'.format(key, value))

        print("""

        save_plot(): Guarda la figura actual en formato .PDF o el formato de elección
         (jpg, png, svg)

        obj.save_plot(<obj.figure> ó <obj.figure_area>, 'nombre_de_figura.pdf')


        save_data(): Guarda el frame actual en formato .CSV

        obj.save_data('<nombre_de_archivo.csv>')
        """)
