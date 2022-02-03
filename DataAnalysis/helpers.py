from os import getcwd, listdir, chdir
import natsort as nsrt

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
