
# OZONATION ANALYSIS AND PLOTTER
# Paquete para graficar los datos obtenidos de la
# ozonización de compuestos utilizando los archivos
# que genera el programa de Matlab.
# Author: F. Javier Morales M.
# Date: 29/11/2021

from os import *
import natsort as nsrt
import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import pandas as pd
import helpers

class Ozonation():

    def __init__(self):
        self.folder


    def ozone_plotter(self, matfile, title='Cinética de Ozonización', width=23, height=15, label='Conc. $O_3$', x0=0, xf=4100, y0=-0.5, yf=35.5, comp='4-Clorofenol', sample=1):
        self.matfile = matfile
        self.title = title
        self.width = cm2in(width)
        self.height = cm2in(height)
        self.label = label
        self.comp = comp
        self.sample = sample
        self.x0 = x0
        self.xf = xf
        self.y0 = y0
        self.yf = yf

        f = h5py.File(self.matfile)
        data = f.get('data')
        data = np.array(data)
        data = pd.DataFrame(data)

        subtitle = f'{self.comp} - Corrida {self.sample}'
        x0 = 0
        xf = 4100
        y0 = -0.5
        yf = 35.5

        fig = data.plot(x=data.columns[0], y=data.columns[1], figsize=[self.width,self.height], label=self.label)
        fig.suptitle(self.title)
        fig.set_title(subtitle, fontsize=14)
        fig.set_xlim(self.x0, self.xf)
        fig.set_ylim(self.y0, self.yf)
        fig.set_xlabel('Tiempo (s)', fontsize=14)
        fig.set_ylabel('$O_3$ [mg/L]', fontsize=14)
        self.ozone_plot = fig.get_figure()
