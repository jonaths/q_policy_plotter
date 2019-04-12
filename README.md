# RL Plotter

A simple package to plot Reinforcement Learning results.

## Dependencies
- Matplotlib
- Pandas

## Installation
1. Clone repository
2. Create or activate Python env.
3. Access policy plotter folder and install locally

```sh
$ cd policy-plotter
$ pip install -e .
```

## Usage
```python
# import dependency
python>> from tools.line_plotter import LinesPlotter
# instantiate
python>> plotter = LinesPlotter(['reward', 'steps', 'end_state'], 1, 1000)
# save each episode with
python>> plotter.add_episode_to_experiment(num_experiment, num_episode,
                                              [
                                                  # reward value at the end of the episode,
                                                  # steps value at the end of the episode,
                                                  # another value at the end of the episode
                                              ])
# create plot from recorded data with moving average and standard deviation
python>> fig, ax = plotter.get_var_line_plot(['reward', 'steps'], 'average', window_size=50)
```

## Examples
See examples folder