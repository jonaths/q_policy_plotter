import matplotlib.pyplot as plt
from plotters.line_plotter import LinesPlotter

plotter = LinesPlotter.load_data('examples/data.npy', ['reward', 'steps', 'end_state'])
fig, ax = plotter.get_var_line_plot(
        ['reward'], 'average', label='reward label')

fig.legend()
plt.tight_layout()
plt.show()