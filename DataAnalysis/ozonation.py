

# from os import *
import natsort as nsrt
import numpy as np
from numpy import trapz
import h5py as h5
import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display, Latex, Math
from DataAnalysis.helpers import *

class Ozonation:

    def __init__(self):
        self.title = 'Cinética de Ozonización'

    def ozone_plotter(self, matfile, var='data',title='Cinética de Ozonización', subtitle=None, xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', label='Conc. $O_3$', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, time='seg', grid=True, visible=True, dx=1.0, **kwargs):

        wcm = cm2in(width)
        hcm = cm2in(height)

        if subtitle == None:
            subtitle = matfile

        f = h5.File(matfile,'r')
        data = f.get(var)
        data = np.array(data)
        self.ozone_allframe = pd.DataFrame(data)
        self.ozone_allframe = self.ozone_allframe.rename(columns={self.ozone_allframe.columns[0]:time, 1:'conc'})
        self.ozone_allframe.index = self.ozone_allframe[time]
        if time == 'min':
            self.ozone_allframe = self.ozone_allframe.rename(columns={self.ozone_allframe.columns[0]:time})
            self.ozone_allframe[time] = self.ozone_allframe[time]/60
            self.ozone_allframe.index = self.ozone_allframe[time]

        elif time == 'h':
            self.ozone_allframe = self.ozone_allframe.rename(columns={self.ozone_allframe.columns[0]:time})
            self.ozone_allframe[time] = self.ozone_allframe[time]/3600
            self.ozone_allframe.index = self.ozone_allframe[time]


        if xf == None:
            xf = max(self.ozone_allframe[time])

        self.ozone_frame = self.ozone_allframe[x0:xf]

        # self.fig = self.ozone_frame[self.x0:self.xf].plot(x=time, y='conc', figsize=[wcm,hcm], label=label, grid=grid, **kwargs)
        self.fig = self.ozone_frame.plot(x=time, y='conc', figsize=[wcm,hcm], label=label, grid=grid, **kwargs)
        plt.suptitle(title, fontsize=14)
        plt.title(subtitle, fontsize=12)
        # fig.set_title(subtitle, fontsize=12)
        self.fig.set_xlim(x0, xf)
        self.fig.set_ylim(y0, yf)
        self.fig.set_xlabel(xlabel+f'({time})', fontsize=12)
        self.fig.set_ylabel(ylabel, fontsize=12)
        self.ozone_plot = self.fig.get_figure()
        # plt.show()
        if visible == False:
            plt.close()
        else:
            plt.show()

        self.area_bc = trapz(x=self.ozone_frame[time][x0:xf], y=self.ozone_frame['conc'][x0:xf], dx=dx)
        self.area_sc = (max(self.ozone_frame[time][x0:xf])*max(self.ozone_frame['conc'][x0:xf]) - self.area_bc)

        if time == 'seg':
            self.area_bc = self.area_bc/60
            self.area_sc = self.area_sc/60
        elif time == 'h':
            self.area_bc = self.area_bc*60
            self.area_sc = self.area_sc*60

        self.ozone_area_bc = r'Ozono no consumido = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.area_bc), max(self.ozone_frame[time][x0:xf])-x0,time)
        self.ozone_area_bc_ltx = Latex(r'Ozono no consumido = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.area_bc),max(self.ozone_frame[time][x0:xf])-x0,time))
        self.ozone_area_sc = r'Ozono consumido = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.area_sc),max(self.ozone_frame[time][x0:xf])-x0,time)
        self.ozone_area_sc_ltx = Latex(r'Ozono consumido = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.area_sc),max(self.ozone_frame[time][x0:xf])-x0,time))
        self.area_t = self.area_bc + self.area_sc
        self.area_total = f'Total ozono generado = {self.area_t:.2f} g/Nm^3 en {max(self.ozone_frame[time][x0:xf])-x0:.0f} {time}'
        self.area_total_ltx = Latex(f'Total ozono generado = $${self.area_t:.2f}~g/Nm^3$$ en {max(self.ozone_frame[time][x0:xf])-x0:.0f} {time}')

        return self.ozone_plot, self.fig, time

def join_plots(frames=list(), labels=list(),title='Cinética de Ozonización', subtitle='', xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', time='min', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, grid=True, visible=True, dx=1.0,**kwargs):
    wcm = cm2in(width)
    hcm = cm2in(height)
    fig, ax = plt.subplots(figsize=[wcm,hcm])
    for frame,label in zip(frames,labels):
        frame.plot(y='conc', ax=ax, label=label)

    plt.suptitle(title, fontsize=14)
    plt.title(subtitle, fontsize=12)
    plt.xlim(x0, xf)
    plt.ylim(y0, yf)
    plt.xlabel(xlabel+f'({time})', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(grid)
    plt.close()
    joined_plots = fig.get_figure()
    return joined_plots
