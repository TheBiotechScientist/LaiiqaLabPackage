

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

    # def __init__(self):
    #     self.title = 'Cinética de Ozonización'

    def plot(self, matfile, var='data',title='Cinética de Ozonización', subtitle=None, xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', label='Conc. $O_3$', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, time='seg', grid=True, visible=True, dx=1.0, **kwargs):
        wcm = cm2in(width)
        hcm = cm2in(height)

        if subtitle == None:
            subtitle = matfile

        f = h5.File(matfile,'r')
        data = f.get(var)
        data = np.array(data)
        self.allframe = pd.DataFrame(data)
        self.allframe = self.allframe.rename(columns={self.allframe.columns[0]:time, 1:'conc'})
        self.allframe.index = self.allframe[time]
        if time == 'min':
            self.allframe = self.allframe.rename(columns={self.allframe.columns[0]:time})
            self.allframe[time] = self.allframe[time]/60
            self.allframe.index = self.allframe[time]

        elif time == 'h':
            self.allframe = self.allframe.rename(columns={self.allframe.columns[0]:time})
            self.allframe[time] = self.allframe[time]/3600
            self.allframe.index = self.allframe[time]


        if xf == None:
            xf = max(self.allframe[time])

        self.frame = self.allframe[x0:xf]

        # fig = self.frame[self.x0:self.xf].plot(x=time, y='conc', figsize=[wcm,hcm], label=label, grid=grid, **kwargs)
        fig = self.frame.plot(x=time, y='conc', figsize=[wcm,hcm], label=label, grid=grid, **kwargs)
        plt.suptitle(title, fontsize=14)
        plt.title(subtitle, fontsize=12)
        # fig.set_title(subtitle, fontsize=12)
        fig.set_xlim(x0, xf)
        fig.set_ylim(y0, yf)
        fig.set_xlabel(xlabel+f'({time})', fontsize=12)
        fig.set_ylabel(ylabel, fontsize=12)
        self.figure = fig.get_figure()
        # plt.show()

        self.area_bc_val = trapz(x=self.frame[time][x0:xf], y=self.frame['conc'][x0:xf], dx=dx)
        self.area_sc_val = (max(self.frame[time][x0:xf])*max(self.frame['conc'][x0:xf]) - self.area_bc_val)

        if time == 'seg':
            self.area_bc_val = self.area_bc_val/60
            self.area_sc_val = self.area_sc_val/60
        elif time == 'h':
            self.area_bc_val = self.area_bc_val*60
            self.area_sc_val = self.area_sc_val*60

        self.area_bc = r'Ozono no consumido = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.area_bc_val), max(self.frame[time][x0:xf])-x0,time)

        self.area_bc_ltx = Latex(r'Ozono no consumido = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.area_bc_val),max(self.frame[time][x0:xf])-x0,time))

        self.area_sc = r'Ozono consumido = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.area_sc_val),max(self.frame[time][x0:xf])-x0,time)

        self.area_sc_ltx = Latex(r'Ozono consumido = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.area_sc_val),max(self.frame[time][x0:xf])-x0,time))

        self.area_t = self.area_bc_val + self.area_sc_val
        self.area_total = f'Total ozono generado = {self.area_t:.2f} g/Nm^3 en {max(self.frame[time][x0:xf])-x0:.0f} {time}'
        self.area_total_ltx = Latex(f'Total ozono generado = $${self.area_t:.2f}~g/Nm^3$$ en {max(self.frame[time][x0:xf])-x0:.0f} {time}')

        if visible == False:
            plt.close()
        else:
            return self.figure.show()

def join_plots(frames=list(), labels=list(),title='Cinética de Ozonización', subtitle='', xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, grid=True, visible=True, dx=1.0,**kwargs):
    wcm = cm2in(width)
    hcm = cm2in(height)
    # fig1 = plt.figure()
    fig, ax = plt.subplots(figsize=[wcm,hcm])
    for frame,label in zip(frames,labels):
        frame.plot(y='conc', ax=ax, label=label)

    time = frames[0].columns[0]
    plt.suptitle(title, fontsize=14)
    plt.title(subtitle, fontsize=12)
    plt.xlim(x0, xf)
    plt.ylim(y0, yf)
    plt.xlabel(xlabel+f'({time})', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.grid(grid)
    joined_plots = fig.get_figure()
    if visible == False:
        plt.close()
    else:
        return joined_plots.show()
