from os import getcwd, listdir, chdir
import natsort as nsrt
import pandas as pd
import matplotlib.pyplot as plt

figuras = r'C:\Users\javne\Dropbox\Tesis Maestria Javier\Tesis\Figuras'
figuras_resultados = r'C:\Users\javne\Dropbox\Tesis Maestria Javier\Tesis\Figuras\resultados'
experimentacion = r'C:\Users\javne\Dropbox\Tesis Maestria Javier\Tesis\Experimentacion'
experimentacion_ozonaciones = r'C:\Users\javne\Dropbox\Tesis Maestria Javier\Tesis\Experimentacion\O3onaciones'
experimentacion_espectrouv = r'C:\Users\javne\Dropbox\Tesis Maestria Javier\Tesis\Experimentacion\EspectroUV'

def where():
    w = getcwd()
    return print(w), nsrt.natsorted(listdir(w))



def cd(folder):
    chdir(folder)
    d = getcwd()
    return print(d), nsrt.natsorted(listdir(d))



def cm2in(value):
    return value/2.54



def save_plot(fig, name):
    fig.savefig(name)



def save_data(self, frame, name):
    frame.to_csv(name, index=frame.index)
    # frame.to_csv(name, index=self.index)

# def join_plots(frames=list(), labels=list(),title='Cinética de Ozonización', subtitle='', xlabel='Tiempo ', ylabel='$O_3$ [$g/Nm^3$]', width=23, height=15, x0=0, xf=None, y0=-0.5, yf=35.5, time='seg', grid=True, visible=True, dx=1.0, **kwargs):
#     wcm = cm2in(width)
#     hcm = cm2in(height)
#     fig, ax = plt.subplots(figsize=[wcm,hcm])
#     ax.grid(grid)
#     for frame,label in zip(frames,labels):
#         frame.plot(y='conc', ax=ax, label=label)
#
#     plt.suptitle(title, fontsize=14)
#     plt.title(subtitle, fontsize=12)
#     plt.xlim(x0, xf)
#     plt.ylim(y0, yf)
#     plt.xlabel(xlabel+f'({time})', fontsize=12)
#     plt.ylabel(ylabel, fontsize=12)
#     plt.close()
#     joined_plots = fig.get_figure()
#     return joined_plots
