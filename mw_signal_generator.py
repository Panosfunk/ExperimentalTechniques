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

            num_iterations = 20
            step = (end_frequency - start_frequency) / num_iterations
            for sig_increment in range(num_iterations):
                current_frequency = start_frequency + step * sig_increment
                freq_values.append(current_frequency)
                freq_bytes = socket.write(f'FREQ {current_frequency}')
                print(sig_increment, 'freq_bytes: ', freq_bytes)

                pow_bytes = socket.write(f'AMPR {power_level}')
                print(sig_increment, 'pow_bytes: ', pow_bytes)

                # Example: Turn on the RF output
                rf_on = socket.write('OUTP ON')
                print(sig_increment, 'rf_on: ', rf_on)
                socket.write('*WAI')

                voltage_values.append(photon_detector_digital_inputs.get_digital_input(rp_ip))

            plt.plot(freq_values, voltage_values)
            plt.title('Voltage vs Frequency')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Voltage (V)')
            plt.show()

            socket.close()
            return freq_values

        else:
            print("Failed to open a TCPIPSocket resource.")

    except pyvisa.errors.VisaIOError as e:
        print(f"Could not connect to the instrument: {e}")
