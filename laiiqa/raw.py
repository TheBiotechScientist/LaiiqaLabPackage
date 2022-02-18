import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from laiiqa.helpers import *


class RawData:

    # frame = pd.DataFrame()

    # def ___init__(self, data):
        # self.data = data
        # self.raw_data(self.data)
        # return self.frame

    # def raw_data(self, data, showframe=False):
    #     # self.data = data
    #     self.frame = pd.DataFrame()
    #     for i in range(len(data)):
    #         self.frame[list(self.data)[i]] = self.data[list(self.data)[i]]
    #
    #     # self.frame.index = self.frame[self.frame.columns[0]]
    #     if showframe == True:
    #         return self.frame

    # @property
    # def frame(self):
    #     return self.frame

    # @frame.setter
    # def frame(self):
    #     return self.frame

    # , secondary_y=False, subplots=False):
    def plot(self, data, title='title=\'Titulo\'', subtitle='subtitle=\'Subtitulo\'', xlabel='xlabel=\'Xlabel\'', ylabel='ylabel=\'Ylabel\'', ylabel2='ylabel2=\'Ylabel 2\'', x=None, width=23, height=15, secondary_y=False, subplots=False, grid=True, interpolation=False, interp='cubic', steps=200, **kwargs):
        self.data = data
        w = cm2in(width)
        h = cm2in(height)

        self.frame = pd.DataFrame()
        for i in range(len(data)):
            self.frame[list(self.data)[i]] = self.data[list(self.data)[i]]


        self.frame.index = self.frame[self.frame.columns[0]]

        if interpolation == True:
            func = dict()
            for i in range(1, len(self.frame.columns)):
                func[i] = interp1d(
                    self.frame.index, self.frame[self.frame.columns[i]], kind=interp)

            self.frame_intp = pd.DataFrame()
            indx = np.linspace(0, max(self.frame[self.frame.columns[0]]), steps)

            for j in range(1, len(self.frame.columns)):
                self.frame_intp[self.frame.columns[j]] = func[j](indx)

            self.frame_intp.index = indx
            if subplots == False:
                fig = self.frame_intp.plot(figsize=(w, h), secondary_y=secondary_y, grid=grid, **kwargs)
                plt.suptitle(title, fontsize=14)
                fig.set_title(subtitle, fontsize=12)
                fig.set_xlabel(xlabel, fontsize=12)
                fig.set_ylabel(ylabel, fontsize=12)
                if secondary_y != False:
                    ylabel2 = secondary_y
                    fig.right_ax.set_ylabel(ylabel2, fontsize=12)

                self.figure = fig.get_figure()
                plt.close()
                return self.figure

            else: #subplots == True:
                color = plt.rcParams["axes.prop_cycle"]()
                fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
                for n in range(0,len(self.frame_intp.columns)):
                    c = next(color)['color']
                    axes[n].plot(self.frame_intp[self.frame_intp.columns[n]], color=c)
                    axes[n].legend([self.frame_intp.columns[n]])
                    axes[n].grid(grid)

                fig.suptitle(title)
                fig.supxlabel(xlabel)
                fig.supylabel(ylabel)
                self.figure = fig.get_figure()
                plt.close()
                return self.figure
        else: # interpolation == False
            if subplots == False:
                fig = self.frame.plot(x=x, figsize=(w, h), secondary_y=secondary_y, grid=grid, **kwargs)
                plt.suptitle(title, fontsize=14)
                fig.set_title(subtitle, fontsize=12)
                fig.set_xlabel(xlabel, fontsize=12)
                fig.set_ylabel(ylabel, fontsize=12)
                if secondary_y != False:
                    ylabel2 = secondary_y
                    fig.right_ax.set_ylabel(ylabel2, fontsize=12)

                self.figure = fig.get_figure()
                plt.close()
                return self.figure

            else: #subplots == True:
                color = plt.rcParams["axes.prop_cycle"]()
                fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)
                for n in range(0,len(self.frame.columns)):
                    c = next(color)['color']
                    axes[n].plot(self.frame[self.frame.columns[n]], color=c)
                    axes[n].legend([self.frame.columns[n]])
                    axes[n].grid(grid)

                fig.suptitle(title)
                fig.supxlabel(xlabel)
                fig.supylabel(ylabel)
                self.figure = fig.get_figure()
                plt.close()
                return self.figure
            # def raw_plotter(self, frame, suptitle='Cinética de Crecimiento', title='',xlabel='Tiempo (h)', ylabel='DO (600nm)', ylabel2='DO (unidades Bug)',c0=1, cf=None,grid=True, linestyle='-', xsize=23, ysize=15, subplots=False, sharex=False,sharey=False):#, time):
            #
            #     # frame.index = frame[frame.columns[0]]
            #     if cf == None:
            #         ycolumn = frame.columns[1:]
            #     else:
            #         ycolumn = frame.columns[1,cf]
            #
            #     # fig= plt.subplots()
            #     fig = frame.plot(x=frame.columns[0], y=ycolumn, grid=grid, linestyle=linestyle,figsize=(cm2in(xsize),cm2in(ysize)), subplots=subplots, sharex=sharex, sharey=sharey)#,xticks=frame[frame.columns[0]])
            #     # fig.plot(frame[frame.columns[0]],frame[frame.columns[3]], label='Promedio')
            #     plt.suptitle(suptitle, fontsize=14)
            #     plt.title(title, fontsize=12)
            #     plt.xlabel(xlabel, fontsize=12)
            #     plt.ylabel(ylabel, fontsize=12)
            #     plt.legend()
            #     # plt.show()
            #     return frame
