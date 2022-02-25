# LAIIQA Laboratory Utilities Package
Librería escrita en Python para el análisis numérico y gráfico de los datos obtenidos de los equipos de ozonización (.mat), espectrofotómetro UV/Vis (.asc) y biorreacciones (.csv), en el Laboratorio de Investigación en Ingeniería Química Ambiental (LAIIQA - ESIQIE - IPN).

## Instalación
Para Python 2, desde la línea de comandos (cmd o  terminal):
```bash
>> pip install laiiqa-lab-utilities
```

Para Python 3:
```bash
>> pip3 install laiiqa-lab-utilities
```
## Uso de la librería
### Obtención de ozonograma
Desde el **IDLE** de **Python**, o **Jupyter Notebook**:

```python{cmd}
import laiiqa.ozonation as oz
import tkinter as tk
from tkinter import filedialog as fd

root = tk.Tk()
root.withdraw()

filetypes = (('MAT-Files', '*.mat'),)

file_path = fd.askopenfilename(
        title='Seleccionar archivo .mat',
        filetypes=filetypes)

c1 = oz.Ozonation()

c1.plot(file_path)
```
