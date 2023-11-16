"""
Script Name: PumpPlot
Description: Capstone Project Computation - Create single plot for pump & system curve
"""
import numpy as np
import matplotlib.pyplot as plt
import time


def accumulator_shift(volume, discharge_time):
    return volume / discharge_time


def pump_curve(Q, Q_max, H_max):
    """ I am using 2nd degree poly formula but change it to whatever """
    return H_max * (1 - ((Q - Q_max) / Q_max) ** 2)


def system_curve(Q, h0, k):
    return h0 + k * Q ** 2


def plot_pump_system_curves(Q_max=300, H_max=300, h=30, k=0.02, Q_shift=15, Q_accumulator_shift=20, volume=0, discharge_time=0,
                            filename="figure.png"):
    Q = np.linspace(0, Q_max * 2, 400)
    Q -= Q_shift
    pump_curves = [
        pump_curve(Q, Q_max, H_max),
        pump_curve(Q, Q_max, H_max * 0.5) + pump_curve(Q, Q_max, H_max * 0.5),
        pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max * 0.5),
        pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max)
    ]

    H_single = pump_curve(Q, Q_max, H_max)
    H_5050 = pump_curve(Q, Q_max, H_max * 0.5) + pump_curve(Q, Q_max, H_max * 0.5)
    H_10050 = pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max * 0.5)
    H_100100 = pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max)
    H_system = system_curve(Q, h, k)
    plt.figure(figsize=(8, 8))

    # Define colors for each curve to use in the plot and legend
    accumulator_colors = ['blue', 'blue', 'blue', 'blue']
    pump_colors = ['cyan', 'cyan', 'cyan', 'cyan']

    # Plotting pump curves
    plt.plot(Q, H_single, color=pump_colors[0], label='Single Pump')
    plt.plot(Q, H_5050, color=pump_colors[1], label='50%+50% Pumps')
    plt.plot(Q, H_10050, color=pump_colors[2], label='100%+50% Pumps')
    plt.plot(Q, H_100100, color=pump_colors[3], label='100%+100% Pumps')

    # Plotting accumulator curves with shifted Q for the accumulator effect
    Q_acc = Q + Q_accumulator_shift
    plt.plot(Q_acc, H_single, '--', color=accumulator_colors[0], label='Single Pump + Acc')
    plt.plot(Q_acc, H_5050, '--', color=accumulator_colors[1], label='50%+50% Pumps + Acc')
    plt.plot(Q_acc, H_10050, '--', color=accumulator_colors[2], label='100%+50% Pumps + Acc')
    plt.plot(Q_acc, H_100100, '--', color=accumulator_colors[3], label='100%+100% Pumps + Acc')

    # Plotting system curve
    plt.plot(Q, H_system, 'r-', label='System Curve')

    # Calculating intersection points and creating legend entries
    custom_legend_handles = []
    curve_names = ["Single Pump", "50%+50% Pumps", "100%+50% Pumps", "100%+100% Pumps"]

    for H_pump, name, pump_color, acc_color in zip(pump_curves, curve_names, pump_colors, accumulator_colors):
        # Intersection for Pump only
        diff_pump_system = H_pump - H_system
        idx_int_pump = np.where(diff_pump_system[:-1] * diff_pump_system[1:] <= 0)[0][-1]
        q_value_pump = Q[idx_int_pump]
        head_value_pump = H_system[idx_int_pump]
        plt.plot(q_value_pump, head_value_pump, 'o', color=pump_color)  # Mark intersection point
        custom_legend_handles.append(plt.Line2D([], [], color=pump_color, marker='o', linestyle='-',
                                                label=f'{name}: Q={q_value_pump:.2f} m³/h, Head={head_value_pump:.2f} m'))

        # Intersection for Pump + Accumulator
        diff_acc_system = H_pump + accumulator_shift(volume,
                                                     discharge_time) - H_system  # Use adjusted head for accumulator
        idx_int_acc = np.where(diff_acc_system[:-1] * diff_acc_system[1:] <= 0)[0][-1]
        q_value_acc = Q_acc[idx_int_acc]
        head_value_acc = H_system[idx_int_acc]
        # plt.plot(q_value_acc, head_value_acc, 'o', color=acc_color)  # Mark intersection point
        custom_legend_handles.append(plt.Line2D([], [], color=acc_color, marker='o', linestyle='--',
                                                label=f'{name} + Acc: Q={q_value_acc:.2f} m³/h, Head={head_value_acc:.2f} m'))

    # Adding the system curve to the legend
    custom_legend_handles.append(plt.Line2D([], [], color='red', linestyle='-', label='System Curve'))

    # Adding the accumulator volume to the legend
    accumulator_info = f"Accumulator Volume: {volume:.2f} Gallon, Discharge interval: {discharge_time} per hr"
    custom_legend_handles.append(plt.Line2D([], [], color='none', label=accumulator_info))

    # Plotting the custom legend
    plt.legend(handles=custom_legend_handles, loc='best', fontsize=8)
    plt.xlabel('Flow Rate (m³/h)')
    plt.ylabel('Head (m)')
    plt.title('Pump and System Curves with Accumulator Effect')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"Plot saved as {filename}")
    plt.close()


# Remove any previous annotations code related to the adjust_text_position function or any calls to it.

def generate_combinations_plot(volumes, discharge_times, Q_max=150, H_max=500, h=30, k=0.02, Q_shift=20):
    iteration = 1
    for volume in volumes:
        for discharge_time in discharge_times:
            shift = accumulator_shift(volume, discharge_time)
            file_name = f"plots/pump_system_Q_{Q_max}_H_{H_max}_shift_{Q_shift}_{iteration}.png"
            iteration += 1
            plot_pump_system_curves(Q_max, H_max, h, k, Q_shift, shift, volume, discharge_time, file_name)
            time.sleep(1)


def main():
    volumes = [1, 3, 5, 7, 8, 10, 12, 15, 30]  # Example volumes
    discharge_times = [0.5, 1, 2, 3, 5, 10, 15, 20, 25, 30]  # Example discharge times
    generate_combinations_plot(volumes, discharge_times)

main()
