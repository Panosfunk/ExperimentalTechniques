import mw_signal_generator


start_frequency = 2.5e9  # Frequency in Hz
end_frequency = 2.95e9  # Frequency in Hz
power_level = 2  # Power level in dBm
rp_ip = '169.254.211.174'

freq_values = mw_signal_generator.send_signal_to_gen(
    start_frequency=start_frequency,
    end_frequency=end_frequency,
    power_level=power_level,
    # one_shot=False
)

# import numpy as np
# import matplotlib.pyplot as plt
#
# file_path = '2.5-2.95 GHz frequency_voltage_data.txt'
# data = np.loadtxt(file_path, delimiter=',', skiprows=1)
#
# frequency = data[:, 0]
# voltage = data[:, 1]
#
# plt.plot(frequency, voltage)
# plt.title('Voltage vs Frequency')
# plt.xlabel('Frequency (GHz)')
# plt.ylabel('Voltage (V)')
# # plt.ylim(0, 0.02)
# plt.show()