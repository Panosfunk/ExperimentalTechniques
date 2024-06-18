import pyvisa

# Create a resource manager
rm = pyvisa.ResourceManager()
pyvisa.log_to_screen()

# Connect to the SG394 using its IP address
generator_ip_address = "169.254.167.111"
port = 5025


def send_signal_to_gen(start_frequency, end_frequency, power_level):
    freq_values = []

    try:
        # Use the open_resource method to get the correct instrument type
        socket = rm.open_resource(f'TCPIP::{generator_ip_address}::{port}::SOCKET',
                                  resource_pyclass=pyvisa.resources.TCPIPSocket)

        print('rm.list_open_resources: ', rm.list_opened_resources())

        # Ensure it is a TCPIPInstrument (if your IDE requires explicit type casting)
        if isinstance(socket, pyvisa.resources.TCPIPSocket):
            # Set the timeout to a reasonable value
            socket.timeout = 100000  # in ms

            num_iterations = 1000
            step = (end_frequency - start_frequency) / num_iterations
            for sig_increment in range(num_iterations):
                current_frequency = start_frequency + step * sig_increment
                freq_values.append(current_frequency)
                freq_bytes = socket.write(f'FREQ {current_frequency}')
                print('freq_bytes: ', freq_bytes)

                pow_bytes = socket.write(f'AMPR {power_level}')
                print('pow_bytes: ', pow_bytes)

                # Example: Turn on the RF output
                rf_on = socket.write('OUTP ON')
                print('rf_on: ', rf_on)
            socket.close()
            return freq_values

        else:
            print("Failed to open a TCPIPSocket resource.")

    except pyvisa.errors.VisaIOError as e:
        print(f"Could not connect to the instrument: {e}")
