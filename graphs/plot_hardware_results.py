#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

" Python script for making all graphs combined at once"

from graphs.lines import *

base_path = '/Users/phisolani/Github/optimal_wifi_slicing/non_linear_optimization/gekko/results/hardware/'

x_axises = []
y1_axises = []
y2_axises = []
# y1_stdevs = []
# y2_stdevs = []

x_axises.append('Time (sec)')
y1_axises.append('Dequeuing rate (p/s)')
y2_axises.append('Throughput (Mbps)')
# y1_stdevs.append('ubmax (STDEV)')
# y2_stdevs.append('TX bytes (STDEV)')

filenames = [base_path + 'ubmax.csv']

draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames,
                                               title='dequeuing_rate_ubmax',
                                               directory='combined',
                                               x_axises=x_axises,
                                               y1_axises=y1_axises,
                                               y2_axises=y2_axises,
                                               x_axis_label='Time (sec)',
                                               y1_axis_label='Dequeuing rate (p/s)',
                                               y2_axis_label='Throughput (Mbps)',
                                               x_axis_limit=330,
                                               y1_axis_limit=3000,
                                               y2_axis_limit=35,
                                               fig_size=[10, 3.4],
                                               annotation_label=r'$\mu^b_{MAX}$ = 1720',
                                               annotation_xy=[65, 20])

filenames_2 = [base_path + 'queue_delay_plot.csv']

x_axises_2 = []
y1_axises_2 = []
y1_expected = []
y2_axises_2 = []

x_axises_2.append('Time (sec)')
y1_axises_2.append('Measured Queueing Delay (ms)')
y1_expected.append('Expected')
y2_axises_2.append('Active Slices')

positions = (70, 100, 150, 200, 250, 300, 330)
labels = ("70", "100", "150", "200", "250", "300", "330")

draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_2,
                                               title='queue_delay_measured_vs_expected',
                                               directory='combined',
                                               x_axises=x_axises_2,
                                               y1_axises=y1_axises_2,
                                               y1_expected=y1_expected,
                                               y2_axises=y2_axises_2,
                                               x_axis_label='Time (sec)',
                                               y1_axis_label='Queueing Delay (ms)',
                                               y2_axis_label='Active Slices',
                                               x_axis_start=70,
                                               x_axis_limit=330,
                                               #y1_axis_limit=100000,
                                               reformulate_xticks=True,
                                               x_pos=positions,
                                               x_labels=labels,
                                               y2_axis_limit=10,
                                               log_scale_x=True,
                                               fig_size=[10, 3.4])

#
# draw_stacked_lines_graph(title='queue_delay',
#                          directory='combined',
#                          fig_size=[10, 3.4])
