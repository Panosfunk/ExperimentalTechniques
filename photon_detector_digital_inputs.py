import redpitaya_scpi as scpi
import numpy as np
import matplotlib.pyplot as plot



def get_digital_input(ip_address):
    rp_s = scpi.scpi(ip_address)

    rp_s.tx_txt('ACQ:RST')

    dec = 4

    # Function for configuring Acquisition
    rp_s.tx_txt('ACQ:RST')

    # Function for configuring Acquisitio
    rp_s.acq_set(dec)

    # For short triggering signals set the length of internal debounce filter in us (minimum of 1 us)
    rp_s.tx_txt('ACQ:TRig:EXT:DEBouncerUs 500')

    rp_s.tx_txt('ACQ:START')
    rp_s.tx_txt('ACQ:TRig EXT_PE')

    while 1:
        rp_s.tx_txt('ACQ:TRig:STAT?')
        if rp_s.rx_txt() == 'TD':
            break

    # ! OS 2.00 or higher only ! #
    while 1:
        rp_s.tx_txt('ACQ:TRig:FILL?')
        if rp_s.rx_txt() == '1':
            break

    # function for Data Acquisition
    buff = rp_s.acq_data(1, convert=True)

    return np.average(buff)
