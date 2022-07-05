import os
from ETL.SAVA.pspython import pspyfiles as ps
from ocp_data import OCP
import matplotlib.pyplot as plt
plt.close('all')

# set path to file
path_to_file = os.path.join('../..', 'data', 'batch1', 'tc2025.pssession')

# Reads measurements and curves from .pssession file
psmeasurements_with_curves = ps.load_session_file(path_to_file, 
                                                  load_peak_data=False, 
                                                  load_eis_fits=False,
                                                  smooth_level=0)

# get measurement and curves
measurement = list(psmeasurements_with_curves.keys())[0]
curves = list(psmeasurements_with_curves.values())[0]
curve = curves[0]

# Print measurement title
print(measurement.Title)

# Print measurement type
print(measurement.meas_type)

# Print curve title
print(curve.Title)

# Print curve type
print(curve.type)

# x is time, y is voltage
time = curve.x_array
voltage = curve.y_array

# OCP data object
ocp_data = OCP(time, voltage)

# calculate drift
results = ocp_data.calculate_drift()
print(results)

# plot
fig, ax = plt.subplots(1, 1, figsize=[12, 8])
ax.plot(ocp_data.time, ocp_data.voltage)
ax.set_ylabel('Voltage [V]')
ax.set_xlabel('Time [s]')
plt.show()
