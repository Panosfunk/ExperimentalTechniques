import pyvisa
import photon_detector_digital_inputs
import matplotlib.pyplot as plt

# Create a resource manager
rm = pyvisa.ResourceManager()
pyvisa.log_to_screen()

# Connect to the SG394 using its IP address
generator_ip_address = "169.254.167.111"
rp_ip = '169.254.211.174'
port = 5025


def send_signal_to_gen(start_frequency, end_frequency, power_level):
    freq_values = []
    voltage_values = []

    try:
        # Use the open_resource method to get the correct instrument type
        socket = rm.open_resource(f'TCPIP::{generator_ip_address}::{port}::SOCKET',
                                  resource_pyclass=pyvisa.resources.TCPIPSocket)

        print('rm.list_open_resources: ', rm.list_opened_resources())

        # Ensure it is a TCPIPInstrument (if your IDE requires explicit type casting)
        if isinstance(socket, pyvisa.resources.TCPIPSocket):
            # Set the timeout to a reasonable value
            socket.timeout = 100000  # in ms

            # Example: Turn on the RF output
            rf_on = socket.write('OUTP ON')
            print('rf_on: ', rf_on)

            num_iterations = 400
            step = (end_frequency - start_frequency) / num_iterations

            file_path = f'{start_frequency/10**9}-{end_frequency/10**9} GHz frequency_voltage_data.txt'

            with open(file_path, 'w') as file:
                file.write('Frequency(Hz), Voltage(V)\n')

                for sig_increment in range(num_iterations):
                    current_frequency = start_frequency + step * sig_increment
                    freq_values.append(current_frequency)
                    freq_bytes = socket.write(f'FREQ {current_frequency}')
                    print(sig_increment, 'freq_bytes: ', freq_bytes)

                    pow_bytes = socket.write(f'AMPR {power_level}')
                    print(sig_increment, 'pow_bytes: ', pow_bytes)

                    socket.write('*WAI')
                    current_voltage = photon_detector_digital_inputs.get_digital_input(rp_ip)

                    file.write(f'{current_frequency/10**9}, {current_voltage/10**9}\n')
                    voltage_values.append(current_voltage)

            plt.plot(freq_values, voltage_values)
            plt.title('Voltage vs Frequency')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Voltage (V)')
            # plt.ylim(0, 0.02)
            plt.show()

            socket.close()
            return freq_values

        else:
            print("Failed to open a TCPIPSocket resource.")

    except pyvisa.errors.VisaIOError as e:
        print(f"Could not connect to the instrument: {e}")
