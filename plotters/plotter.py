import numpy as np
import matplotlib.pyplot as plt
from helpers import heatmap,annotate_heatmap
import sys


class PolicyPlotter:

    def __init__(self, table, num_rows, num_cols):
        pass
        self.table = table
        self.num_rows = num_rows
        self.num_cols = num_cols

    def summarize(self, op='max'):
        """
        Ejecuta una operacion sobre el valor de las acciones de un estado.
        :param op: max, min o avg.
        :return: np.array con shape (states, 1)
        """
        if op is 'max':
            summary = np.max(self.table, axis=1)
        elif op is 'min':
            summary = np.min(self.table, axis=1)
        elif op is 'avg':
            summary = np.average(self.table, axis=1)
        else:
            raise Exception('Invalid op')
        return summary.reshape(self.table.shape[0], -1)

    def get_policy(self, labels=None):
        """
        Calcula la politica (max_arg) segun self.table.
        :param labels: una lista con el nombre de los acciones en el mismo orden que
        estan en table.
        :return: Lista con shape (states, 1)
        """
        summary = np.max(self.table, axis=1)
        indices = np.argmax(self.table, axis=1)
        if labels is not None:
            temp = []
            for i in range(self.table.shape[0]):
                temp.append(labels[indices[i]])
            indices = temp
        return list(summary), indices

    def build_heatmap(self, op='max', index=None, annotate=True, cmap='Blues'):
        """
        Crea un heatmap con una operacion. Por default max. La esquina inferior
        derecha es el elemento cero, (1,0)=1, (2,0)=2, (3,0)=3.
        :param num_rows: las filas del gridworld
        :param num_cols: las columnas del gridworld
        :param op: la operacion. Las mismas que self.summarize.
        :return:
        """
        if self.num_cols * self.num_rows != self.table.shape[0]:
            raise Exception('Table shape 0 and num_rows x num_cols do not match. ')
        if index is not None:
            # si se pasa un index recupera la accion de ese index
            summary = self.table[:, index]
        else:    
            # de lo contrario calcula el summary segun op
            summary = self.summarize(op)
        summary_grid = summary.reshape((self.num_cols, self.num_rows))
        summary_grid = np.transpose(summary_grid)
        im, cbar = heatmap(summary_grid, range(self.num_rows), range(self.num_cols), cmap=cmap)
        if annotate:
	        annotate_heatmap(im)
        # plt.ylim(plt.ylim()[::-1])

        return im, cbar

    def build_policy(self, labels=None, show_numbers=True, cmap='Blues'):
        if self.num_cols * self.num_rows != self.table.shape[0]:
            raise Exception('Table shape 0 and num_rows x num_cols do not match. ')
        summary, indices = self.get_policy(labels)

        summary_grid = np.array(summary).reshape((self.num_cols, self.num_rows))
        summary_grid = np.transpose(summary_grid)

        indices_grid = [['x' for col in range(self.num_cols)] for row in range(self.num_rows)]
        for i in range(len(indices)):
            quotient = i // self.num_rows
            remainder = i % self.num_rows
            indices_grid[remainder][quotient] = indices[i]

        im, cbar = heatmap(summary_grid, range(self.num_rows), range(self.num_cols), cmap=cmap)
        # plt.ylim(plt.ylim()[::-1])
        texts = annotate_heatmap(im, adds=indices_grid, show_numbers=show_numbers)

        return im, cbar, texts
