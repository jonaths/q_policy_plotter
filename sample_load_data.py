import matplotlib.pyplot as plt
from plotters.line_plotter import LinesPlotter
import numpy as np

# lee un resultado que contiene tres campos
plotter = LinesPlotter.load_data('examples/data_small.npy',
                                 ['reward', 'steps', 'end_state'])

# grafica el campo reward asignando la etiqueta reward label a la grafica
# al calcular average grafica std dev tambien
fig, ax = plotter.get_var_line_plot(
        ['reward'], 'average', label='reward label', window_size=2)

fig.legend()
plt.tight_layout()
plt.show()
