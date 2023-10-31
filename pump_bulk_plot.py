"""
Script Name: PumpBulkPlot
Description: Capstone Project Computation - Calculation and Visualization for Pump & Accumulator conditions
"""
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, timezone

def accumulator_shift(volume, discharge_time):
    return volume / discharge_time


def pump_curve(Q, Q_max, H_max, efficiency=1.0):
    return H_max * (1 - ((Q - Q_max) / Q_max) ** 2) * efficiency


def system_curve(Q, h0, k):
    return h0 + k/3 * Q ** 2


def find_intersection(Q, H_pump, H_system):
    """ There is probably smarter way to implement this part"""
    for i in range(1, len(Q)):
        if H_pump[i] < H_system[i]:

            m1 = (H_pump[i] - H_pump[i - 1]) / (Q[i] - Q[i - 1])
            c1 = H_pump[i] - m1 * Q[i]

            m2 = (H_system[i] - H_system[i - 1]) / (Q[i] - Q[i - 1])
            c2 = H_system[i] - m2 * Q[i]
            intersection_Q = (c2 - c1) / (m1 - m2)
            return intersection_Q
    return None


def plot_pump_system_curves(ax, Q_max=200, H_max=300, h=20, k=0.02, Q_shift=10, Q_accumulator_shift=15, efficiency1=1.0,
                            efficiency2=1.0):
    Q = np.linspace(0, 200, 400)
    Q -= Q_shift
    H_single = efficiency1 * pump_curve(Q, Q_max, H_max)
    H_system = system_curve(Q, h, k)

    intersection_flow = find_intersection(Q, H_single, H_system)

    ax.plot(Q, H_single, label=f"Eff {efficiency1 * 100:.0f}%")
    ax.plot(Q + Q_accumulator_shift, H_single, linestyle='--',
            label=f"Eff {efficiency1 * 100:.0f}% w/ Acc")
    ax.plot(Q, H_system, 'k-', label='System Curve')
    ax.legend(loc="upper right")

    return intersection_flow


def generate_combinations_plot(volumes, discharge_times, efficiencies, Q_max=100, H_max=300, h=30, k=0.02, Q_shift=15, filename="figure.png"):
    table_data = [["Volume", "Discharge Time (min)", "Efficiency", "Flow Rate (m^3/min)"]]
    num_subplots = len(volumes) * len(discharge_times) * len(efficiencies)
    cols = 10
    rows = int(np.ceil(num_subplots / cols))

    fig, axs = plt.subplots(rows, cols, figsize=(15, 5 * rows))

    plot_index = 0
    for volume in volumes:
        for discharge_time in discharge_times:
            accumulator_shift_value = accumulator_shift(volume, discharge_time)
            for eff in efficiencies:
                row, col = divmod(plot_index, cols)
                ax = axs[row][col] if rows > 1 else axs[col]

                ax.set_ylim([50, 400]) # We can change it depending on dataset dimensions
                flow_rate = plot_pump_system_curves(ax, Q_max, H_max, h, k, Q_shift, accumulator_shift_value, eff, eff)
                table_data.append([volume, discharge_time, f"{eff * 100:.1f}%", f"{flow_rate:.2f}"])
                plot_index += 1

    # For any unused subplots
    for i in range(plot_index, rows * cols):
        row, col = divmod(i, cols)
        (axs[row][col] if rows > 1 else axs[col]).remove()

    # Display table
    ax_table = fig.add_axes([0.1, 0, 0.8, 0.2])
    ax_table.axis("off")
    table = ax_table.table(cellText=table_data, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    fig.subplots_adjust(bottom=0.25)  # make room for table

    CST = timezone(timedelta(hours=-5))
    time_now = datetime.now(CST)
    current_datetime = time_now.strftime("%Y-%m-%d %H:%M:%S")
    fig.suptitle(f"Possible Pump & Accumulator Variations\nResults Generated at {current_datetime} @TAMU ETID Capstone Project Rev", fontsize=15)  # Add the super title here
    plt.savefig(filename)


def main():
    # Condition 1 - Fixed eff
    volumes1 = [5, 10, 15, 20]
    discharge_times1 = [1, 2, 3, 4, 5]
    efficiencies1 = [1.0]  # 100% efficiency
    generate_combinations_plot(volumes1, discharge_times1, efficiencies1, filename="single_pump_accu_variables.png")

    # Condition 2 -  Fixed acc
    volumes2 = [5]
    discharge_times2 = [3]
    efficiencies2 = [1.0, 1.25, 1.5, 1.75, 2.0]  # Efficiency values provided
    generate_combinations_plot(volumes2, discharge_times2, efficiencies2, filename="double_pump_eff_variables.png")

    # Condition 3 - Mixed
    volumes3 = [3, 5, 10, 15]
    discharge_times3 = [1, 3, 5]
    efficiencies3 = [1.0, 1.5, 2.0]  # Efficiency values provided
    generate_combinations_plot(volumes3, discharge_times3, efficiencies3, filename="pump_acc_mix_variables.png")

    # We can add more later

main()

