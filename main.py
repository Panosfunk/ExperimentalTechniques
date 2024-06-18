import mw_signal_generator


start_frequency = 1e8  # Frequency in Hz
end_frequency = 2e8  # Frequency in Hz
power_level = 5  # Power level in dBm
rp_ip = '169.254.211.174'

# photon_detector_signal_input.connect_to_pitaya()

freq_values = mw_signal_generator.send_signal_to_gen(
    start_frequency=start_frequency,
    end_frequency=end_frequency,
    power_level=power_level,
    # one_shot=False
)

# mw_signal_generator.send_signal_to_gen(start_frequency, end_frequency, power_level)

# buff = photon_detector_digital_inputs.get_digital_input(rp_ip)
#
# plot.plot(buff)
# plot.xlabel('Freq')
# plot.ylabel('Voltage')
# plot.show()
