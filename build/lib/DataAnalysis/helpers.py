from os import *
import natsort as nsrt

def dir():
    return getcwd()



def cd(folder):
    chdir(folder)
    return nsrt.natsorted(listdir(getcwd()))



def cm2in(value):
    return value/2.54



def save_plot(fig, name):
    fig.savefig(name)



def save_data(self, frame, name):
    frame.to_csv(name, index=frame.index)
    # frame.to_csv(name, index=self.index)
