import numpy as np
import sys
import matplotlib.pyplot as plt


class LinesPlotter:

    def __init__(self, var_names_list, num_experiments, num_episodes):
        pass
        self.var_names_list = var_names_list
        self.num_episodes = num_episodes
        self.num_experiments = num_experiments
        self.data = np.zeros(shape=(num_experiments, num_episodes, len(var_names_list)))
        self.summary = None
        self.std_dev = None
        # avg + 1/2 std_dev
        self.std_dev_top = None
        # avg - 1/2 std_dev
        self.std_dev_bottom = None

    def add_episode_to_experiment(self, experiment, episode, var_values):
        """
        Agrega un episodio al experimento
        :param experiment: el numero de experimento
        :param episode: el numero de episodio
        :param var_values: una lista de valores en el mismo orden que var_name_list
        :return:
        """
        if experiment >= self.num_experiments or episode >= self.num_episodes:
            return self
        self.data[experiment, episode, :] = np.array(var_values)
        return self

    def calculate_summary(self, func='average'):
        """
        Crea un summary de los valores almacenados en el historial
        :param func: la operacion de summary (average, max)
        :return:
        """
        temp = np.transpose(self.data, (2, 1, 0))
        print(temp)
        if func == 'average':
            self.summary = np.average(temp, axis=2)
            self.std_dev = np.std(temp, axis=2)
            half = self.std_dev / 2
            self.std_dev_top = self.summary + half
            self.std_dev_bottom = self.summary - half
        elif func == 'max':
            self.summary = np.max(temp, axis=2)
        else:
            raise Exception('Invalid summary operation')

        return self

    def get_var_from_summary(self, var_name):
        """
        Wrapper para get_var_from_array que recupera la variable de self.summary
        :param var_name:
        :return:
        """
        return self.get_var_from_array(var_name, self.summary)

    def get_var_from_array(self, var_name, array):
        """
        Usa los nombres creados en el constructor para recuperar los valores
        de una variable
        :param var_name: el nombre de la variable
        :param array:
        :return:
        """
        # Si se pasa un valor regresa unicamente ese elemento
        if var_name in self.var_names_list:
            index = self.var_names_list.index(var_name)
            summary_pickled = np.expand_dims(array[index], axis=0)
        else:
            raise Exception('Invalid var_name. ')
        return summary_pickled

    def get_var_from_data(self, var_name):
        # Si se pasa un valor regresa unicamente ese elemento
        if var_name in self.var_names_list:
            index = self.var_names_list.index(var_name)
            data_pickled = self.data[:, :, index]
        else:
            raise Exception('Invalid var_name. ')
        return data_pickled

    @staticmethod
    def convolve(data, window_size):
        """
        Media movil
        :param data: la serie de datos
        :param window_size: el tamano de la ventana movil
        :return:
        """
        data = np.pad(data, (window_size // 2, window_size - 1 - window_size // 2), mode='edge')
        data = np.convolve(data, np.ones((window_size,)) / window_size, mode='valid')
        return data

    def get_var_line_plot(self, var_name_list, func, linestyle=None, window_size=20, fig=None,
                          ax=None, label=None):
        """
        Genera una grafica lineal con los datos de los experimentos procesados con alguna funcion
        summary,
        :param label:
        :param var_name_list: las variables del experimento a recuperar.
        :param func: la funcion summary
        :param linestyle: el estilo de linea de la serie
        :param window_size: tamano de la ventana
        :param fig: on objeto figura o lo crea
        :param ax: un objeto ax o lo crea
        :return:
        """
        if fig is None and ax is None:
            fig, ax = plt.subplots()
        self.calculate_summary(func)
        for var_name in var_name_list:

            label = var_name if label is None else label

            data = self.get_var_from_summary(var_name)[0]
            data = self.convolve(data, window_size)

            if linestyle is None:
                ax.plot(range(self.num_episodes), data, label=label)
            else:
                ax.plot(range(self.num_episodes), data, label=label, linestyle=linestyle)

            # grafica la desviacion estandar si es un promedio
            if self.std_dev_top is not None and self.std_dev_bottom is not None:
                top = self.get_var_from_array(var_name, self.std_dev_top)[0]
                top = self.convolve(top, window_size)
                bottom = self.get_var_from_array(var_name, self.std_dev_bottom)[0]
                bottom = self.convolve(bottom, window_size)
                ax.fill_between(range(self.num_episodes), bottom, top, alpha=0.25)




        return fig, ax

    def get_var_cummulative_matching_plot(self, var_name, matching_list, linestyle=None, fig=None,
                                          ax=None, label=None):
        """
        Recibe matching_list y verifica los valores en var_name de data. Genera un acumulado.
        :param label:
        :param ax:
        :param fig:
        :param linestyle:
        :param var_name: el nombre de la variable a contar
        :param matching_list: los valores que cuentan como 1
        :return:
        """

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        data = self.get_var_from_data(var_name)

        # compara con la lista y pone 1 si esta
        test = np.isin(data, matching_list).astype(int)
        # suma acumulada a traves de cada experimento
        test = np.cumsum(test, axis=1)
        # promedio de todos los experimentos
        test = np.average(test, axis=0)

        label = var_name if label is None else label

        if linestyle is None:
            ax.plot(range(self.num_episodes), test, label=label)
        else:
            ax.plot(range(self.num_episodes), test, label=label, linestyle=linestyle)
        return fig, ax

    def get_pie_plot(self, var_name, mapping_dict):
        """
        Cuenta los elementos de una lista y los agrupa segun mapping_dict. Si alguna falta
        le asigna la etiqueta other.
        :param var_name:
        :param mapping_dict:
        :return:
        """

        fig, ax = plt.subplots()
        data = self.get_var_from_data(var_name)
        data = data.astype(int).flatten().tolist()
        data_copy = data[:]

        labels = mapping_dict.keys()

        count = []
        for l in labels:
            c = 0
            for d in range(len(data)):
                if data[d] in mapping_dict[l]:
                    c += 1
                    data_copy.remove(data[d])
            count.append(c)

        labels.append('other')
        count.append(len(data_copy))

        ax.pie(count, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        return fig, ax

    def save_data(self, name):
        numpy_data = np.array(self.data)
        np.save(name, numpy_data)
        return self

    @staticmethod
    def load_data(name, var_name_list=None, num_episodes=None):
        """
        Carga un archivo de datos y crea un objeto LinesPlotter
        :param num_episodes:
        :param name: el nombre del archivo que contiene los datos guardado con save_data()
        :param var_name_list: el nombre de los datos guardados. Si no esta les asigna un entero.
        :return:
        """
        if num_episodes is None:
            data = np.load(name)
        else:
            data = np.load(name)[:, 0:num_episodes, :]
        print(data.shape)
        num_experiments = data.shape[0]
        num_episodes = data.shape[1]

        if var_name_list is None:
            var_name_list = [str(i) for i in range(data.shape[2])]
        elif len(var_name_list) != data.shape[2]:
            raise Exception('Invalid var_name_list. Must have len' + str(data.shape[2]))

        plotter = LinesPlotter(var_name_list, num_experiments, num_episodes)
        plotter.data = data
        print('Data loaded. Shape:')
        print(data.shape)
        return plotter
