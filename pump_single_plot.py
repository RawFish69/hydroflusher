"""
Script Name: PumpSinglePlot
Description: Capstone Project Computation - Create single plot for pump & system curve
"""
import numpy as np
import matplotlib.pyplot as plt


def accumulator_shift(volume, discharge_time):
    return volume / discharge_time

def pump_curve(Q, Q_max, H_max):
    """ Im using 2nd degree poly formula but change it to whatever """
    return H_max * (1 - ((Q - Q_max) / Q_max) ** 2)

def system_curve(Q, h0, k):
    return h0 + k * Q ** 2


def plot_pump_system_curves(Q_max=100, H_max=300, h=30, k=0.02, Q_shift=15, Q_accumulator_shift=20):
    # Constants -> Replaced by parameters upon calling this function
    # Below is for testing purpose ONLY
    # Q_max = 100
    # H_max = 300
    # h = 30
    # k = 0.02
    # Q_shift = 15
    # Q_accumulator_shift = 20
    # Flow rate range (extended for a longer system curve)
    Q = np.linspace(0, 200, 400)
    # Flow offset
    Q -= Q_shift
    # Pump curves, number represent eff % ratio
    H_single = pump_curve(Q, Q_max, H_max)
    H_5050 = pump_curve(Q, Q_max, H_max * 0.5) + pump_curve(Q, Q_max, H_max * 0.5)
    H_10050 = pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max * 0.5)
    H_100100 = pump_curve(Q, Q_max, H_max) + pump_curve(Q, Q_max, H_max)
    H_system = system_curve(Q, h, k)
    plt.figure(figsize=(8, 8))

    pump_curves = [H_single, H_5050, H_10050, H_100100]
    accumulator_curves = [H_single, H_5050, H_10050, H_100100]
    accumulator_Q_values = [Q + Q_accumulator_shift for _ in pump_curves]
    curve_names = ["Single Pump", "50%+50% Pumps", "100%+50% Pumps", "100%+100% Pumps"]
    accumulator_names = [name + " with accumulator" for name in curve_names] # Replaced by short_curve_names
    # Manual offsets - Adjust as needed
    offsets = [(30, 10), (30, -20), (-30, 10), (-30, -20)]
    # Display names here, don't name it too long
    short_curve_names = ["100%+100%", "100%+50%", "Single P.", "50%+50%"]
    short_acc_names = [name + " + Acc" for name in short_curve_names]
    annotated_intersections = []
    threshold = 0.5  # Edge cases
    for H_pump, Q_acc, H_acc, name, acc_name, offset in zip(pump_curves, accumulator_Q_values, accumulator_curves, short_curve_names, short_acc_names, offsets):
        plt.plot(Q, H_pump, 'b-', label=name)
        plt.plot(Q_acc, H_acc, 'c-', label=acc_name)
        # Intersection between Pump and System Curve
        diff_pump_system = H_pump - H_system
        idx_int_pump = np.where(diff_pump_system[:-1] * diff_pump_system[1:] <= 0)[0][-1]
        # Check if the intersection is too close to an already annotated intersection
        if not any(abs(Q[idx_int_pump] - annotated_Q) < threshold for annotated_Q in annotated_intersections):
            plt.plot(Q[idx_int_pump], H_system[idx_int_pump], 'go')
            plt.annotate(f'{name}\nQ={Q[idx_int_pump]:.2f} m^3/h',
                         (Q[idx_int_pump], H_system[idx_int_pump]),
                         textcoords="offset points",
                         xytext=offset,
                         ha='center',
                         fontsize=8,
                         # bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor="aliceblue"),
                         arrowprops=dict(facecolor='black', arrowstyle='->'))
            annotated_intersections.append(Q[idx_int_pump])
        # Intersection between Pump+Accumulator and System Curve
        diff_acc_system = H_acc - H_system
        idx_int_acc = np.where(diff_acc_system[:-1] * diff_acc_system[1:] <= 0)[0][-1]
        if not any(abs(Q_acc[idx_int_acc] - annotated_Q) < threshold for annotated_Q in annotated_intersections):
            plt.plot(Q_acc[idx_int_acc], H_system[idx_int_acc], 'go')
            plt.annotate(f'{acc_name}\nQ={Q_acc[idx_int_acc]:.2f}',
                         (Q_acc[idx_int_acc], H_system[idx_int_acc]),
                         textcoords="offset points",
                         xytext=offset,
                         ha='center',
                         fontsize=8,
                         # bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor="aliceblue"),
                         arrowprops=dict(facecolor='black', arrowstyle='->'))
            annotated_intersections.append(Q_acc[idx_int_acc])
    plt.legend(loc='upper left')
    plt.plot(Q, H_system, 'r', label='System Curve')
    plt.legend(['Pump Curve', 'Pump + Accumulator Curve', 'System Curve'])
    plt.xlabel('Flow Rate (m^3/h)')
    plt.ylabel('Head (m)')
    plt.xlim([75, 175])
    plt.ylim([100, 800])
    plt.title('Pump and System Curves with Accumulator Effect')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def generate_combinations_plot(volumes, discharge_times, Q_max=100, H_max=300, h=30, k=0.02, Q_shift=15):
    for volume in volumes:
        for discharge_time in discharge_times:
            shift = accumulator_shift(volume, discharge_time)
            plot_pump_system_curves(Q_max, H_max, h, k, Q_shift, shift)


def main():
    volumes = [10, 20, 30, 40, 50]  # Example volumes
    discharge_times = [1, 2, 3, 4, 5]  # Example discharge times
    generate_combinations_plot(volumes, discharge_times)


main()
