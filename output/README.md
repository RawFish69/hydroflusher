
### Components of the File Name

- `Q_{Q_max}`: Represents the maximum flow rate (Q_max) used in the plot.
- `H_{H_max}`: Indicates the maximum head (H_max) value used.
- `shift_{Q_shift}`: Denotes the shift in the flow rate (Q_shift).
- `{iteration}`: A sequential number representing the iteration of the plot in a series.

### Example

Given the parameters `Q_max=150`, `H_max=200`, `Q_shift=20`, and iterating over different volumes and discharge times, the file names will be structured as follows:


## Plot Generation Script

The file names are generated within the `generate_combinations_plot` function, which iterates over a range of volumes and discharge times to produce a series of plots. Each plot corresponds to a different combination of parameters.

```python
def generate_combinations_plot(volumes, discharge_times, Q_max=150, H_max=200, h=20, k=0.0025, Q_shift=20):
    """Execute combination plot generation"""
    for i, volume in enumerate(volumes):
        for j, discharge_time in enumerate(discharge_times):
            iteration = i * len(discharge_times) + j + 1
            shift = accumulator_shift(volume, discharge_time)
            file_name = f"pump_system_Q_{Q_max}_H_{H_max}_shift_{Q_shift}_{iteration}.png"
            plot_pump_system_curves(Q_max, H_max, h, k, Q_shift, shift, volume, discharge_time, file_name)
            time.sleep(1)

```
