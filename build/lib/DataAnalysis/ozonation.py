

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

    def plot(self, matfile, var='data',title='Cinética de Ozonización', subtitle=None, xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', label='Conc. $O_3$', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, time='seg', units='g/nm3',grid=True, visible=True, dx=1.0, **kwargs):
        self.time = time
        wcm = cm2in(width)
        hcm = cm2in(height)

        if subtitle == None:
            subtitle = matfile

        f = h5.File(matfile,'r')
        data = np.array(f.get(var))
        self.frameall = pd.DataFrame(data)
        self.frameall = self.frameall.rename(columns={self.frameall.columns[0]:time, 1:'conc'})
        self.frameall.index = self.frameall[time]
        if time == 'min':
            self.frameall = self.frameall.rename(columns={self.frameall.columns[0]:time})
            self.frameall[time] = self.frameall[time]/60
            self.frameall.index = self.frameall[time]

        elif time == 'h':
            self.frameall = self.frameall.rename(columns={self.frameall.columns[0]:time})
            self.frameall[time] = self.frameall[time]/3600
            self.frameall.index = self.frameall[time]


        if xf == None:
            xf = max(self.frameall[time])

        self.frame = self.frameall[x0:xf]

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

        self.residual = trapz(x=self.frame[time][x0:xf], y=self.frame['conc'][x0:xf], dx=dx)
        self.consumido = (max(self.frame[time][x0:xf])*max(self.frame['conc'][x0:xf]) - self.residual)


        if time == 'seg':
            self.residual = self.residual/60
            self.consumido = self.consumido/60
        elif time == 'h':
            self.residual = self.residual*60
            self.consumido = self.consumido*60

        # Agregar la opción de unidades g/Nm3 o g/L
        if units == 'g/nm3':
            self.residual_print = r'Ozono residual = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.residual), max(self.frame[time][x0:xf])-x0,time)

            self.residual_latex = Latex(r'Ozono residual = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.residual),max(self.frame[time][x0:xf])-x0,time))

            self.consumido_print = r'Ozono consumido = {0:.2f} g/Nm^3 en {1:.0f} {2}'.format(float(self.consumido),max(self.frame[time][x0:xf])-x0,time)

            self.consumido_latex = Latex(r'Ozono consumido = $${0:.2f}~g/Nm^3$$ en {1:.0f} {2}'.format(float(self.consumido),max(self.frame[time][x0:xf])-x0,time))

            self.total = self.residual + self.consumido
            self.total_print = f'Total ozono generado = {self.total:.2f} g/Nm^3 en {max(self.frame[time][x0:xf])-x0:.0f} {time}'
            self.total_latex = Latex(f'Total ozono generado = $${self.total:.2f}~g/Nm^3$$ en {max(self.frame[time][x0:xf])-x0:.0f} {time}')

        if units == 'g/l':
            self.residual = self.residual/1000
            self.consumido = self.consumido/1000

            self.residual_print = r'Ozono residual = {0:.2f} g/L en {1:.0f} {2}'.format(float(self.residual), max(self.frame[time][x0:xf])-x0,time)

            self.residual_latex = Latex(r'Ozono residual = $${0:.2f}~g/L$$ en {1:.0f} {2}'.format(float(self.residual),max(self.frame[time][x0:xf])-x0,time))

            self.consumido_print = r'Ozono consumido = {0:.2f} g/L en {1:.0f} {2}'.format(float(self.consumido),max(self.frame[time][x0:xf])-x0,time)

            self.consumido_latex = Latex(r'Ozono consumido = $${0:.2f}~g/L$$ en {1:.0f} {2}'.format(float(self.consumido),max(self.frame[time][x0:xf])-x0,time))

            self.total = self.residual + self.consumido
            self.total_print = f'Total ozono generado = {self.total:.2f} g/L en {max(self.frame[time][x0:xf])-x0:.0f} {time}'
            self.total_latex = Latex(f'Total ozono generado = $${self.total:.2f}~g/L$$ en {max(self.frame[time][x0:xf])-x0:.0f} {time}')

        if visible == False:
            plt.close()
        else:
            plt.show()



    def join(self, frames=list(), labels=list(),title='Cinética de Ozonización', subtitle='', xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, grid=True, visible=True, dx=1.0,**kwargs):
        wcm = cm2in(width)
        hcm = cm2in(height)
        # fig1 = plt.figure()
        fig, ax = plt.subplots(figsize=[wcm,hcm])
        for frame,label in zip(frames,labels):
            frame.plot(y='conc', ax=ax, label=label)

        # time = frames[0].columns[0]
        plt.suptitle(title, fontsize=14)
        plt.title(subtitle, fontsize=12)
        plt.xlim(x0, xf)
        plt.ylim(y0, yf)
        plt.xlabel(xlabel+f'({self.time})', fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.grid(grid)
        self.joined_plots = fig.get_figure()
        if visible == False:
            plt.close()
        else:
            plt.show()
            # return self.joined_plots
