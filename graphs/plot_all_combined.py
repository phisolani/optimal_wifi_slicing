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

base_path = '/Users/phisolani/Github/optimal_wifi_slicing/non_linear_optimization/gekko/results/'
z3_base_path = '/Users/phisolani/Github/optimal_wifi_slicing/theorem_prover/z3/results/'
# algorithm_base_path = '/Users/phisolani/Github/optimal_wifi_slicing/heuristics/DWFAA/results/'

solvers = ['IPOPT', 'APOPT']
APOPT_local = False  # True or False

filenames_optimal_equal = []
# filenames_optimal_scalar = []

filenames_feasible_equal = []
# filenames_feasible_scalar = []

x_axises = []
y1_axises = []
y2_axises = []
y1_stdevs = []
y2_stdevs = []

for s in solvers:
    x_axises.append('Number of Slices (#)')
    y1_axises.append(str(s) + ' Objective (ms)')
    y2_axises.append(str(s) + ' Solution Time (sec)')
    y1_stdevs.append(str(s) + ' Objective (STDEV)')
    y2_stdevs.append(str(s) + ' Solution Time (STDEV)')

    where = 'remote'

    if APOPT_local:
        if s == 'APOPT':
            where = 'local'

    filenames_optimal_equal.append(
        str(base_path) + 'processed_results_' + str(where) + '_' + str(s) + '_equal_optimality.csv')
    # filenames_optimal_scalar.append(str(base_path) + 'processed_results_' + str(where) + '_' + str(s) + '_scalar_optimality.csv')

    filenames_feasible_equal.append(
        str(base_path) + 'processed_results_' + str(where) + '_' + str(s) + '_equal_feasibility.csv')
    # filenames_feasible_scalar.append(str(base_path) + 'processed_results_' + str(where) + '_' + str(s) + '_scalar_feasibility.csv')

# For the algorithm together
# x_axises.append('Number of Slices (#)')
# y1_axises.append('DWFAA Objective (sec)')
# y2_axises.append('DWFAA Solution Time (sec)')
# y1_stdevs.append('DWFAA Objective (STDEV)')
# y2_stdevs.append('DWFAA Solution Time (STDEV)')

# filenames_optimal_equal.append(algorithm_base_path + 'processed_results_equal_DWFAA.csv')
# filenames_optimal_scalar.append(algorithm_base_path + 'processed_results_scalar_DWFAA.csv')

draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_equal,
                                               title=str(solvers[0]) + '_vs_' + str(solvers[1]) + '_equal_optimality',
                                               directory='combined',
                                               x_axises=x_axises,
                                               y1_axises=y1_axises,
                                               y2_axises=y2_axises,
                                               x_axis_label='Number of Slices',
                                               y1_axis_label='Objective (ms)',
                                               y2_axis_label='Solution Time (sec)',
                                               y1_stdevs=y1_stdevs,
                                               y2_stdevs=y2_stdevs,
                                               fig_size=[10, 3.4],
                                               markers=['^', 'o'],
                                               log_scale_y=True)

# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_equal,
#                                                     title=str(solvers[0]) + ' vs ' + str(solvers[1]) + '_equal_optimality_(Zoom)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=8,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
#
# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_equal,
#                                                     title=str(solvers[0]) + '_vs_' + str(solvers[1]) + '_equal_optimality_(Zoom +)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=2,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)


# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_scalar,
#                                                     title=str(solvers[0]) + '_vs_' + str(solvers[1]) + '_scalar_optimality',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y1_axis_limit=600,
#                                                     y2_axis_limit=80,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)

# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_scalar,
#                                                     title=str(solvers[0]) + '_vs_' + str(solvers[1]) + '_scalar_optimality_(Zoom)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=8,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
#
# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_optimal_scalar,
#                                                     title=str(solvers[0]) + '_vs_' + str(solvers[1]) + '_scalar_optimality_(Zoom +)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=2,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)

# Removing algorithm
# x_axises.pop()
# y1_axises.pop()
# y2_axises.pop()
# y1_stdevs.pop()
# y2_stdevs.pop()

# Removing Solvers...
x_axises.pop()
y1_axises.pop()
y2_axises.pop()
y1_stdevs.pop()
y2_stdevs.pop()
x_axises.pop()
y1_axises.pop()
y2_axises.pop()
y1_stdevs.pop()
y2_stdevs.pop()

filenames_feasible_equal.pop()
filenames_feasible_equal.pop()

# To include Z3
filenames_feasible_equal.append(str(z3_base_path) + 'processed_results_equal_z3.csv')
# filenames_feasible_scalar.append(str(z3_base_path) + 'processed_results_scalar_z3.csv')

x_axises.append('Number of Slices (#)')
y1_axises.append('Z3 Objective (ms)')
y2_axises.append('Z3 Solution Time (sec)')
y1_stdevs.append('Z3 Objective (STDEV)')
y2_stdevs.append('Z3 Solution Time (STDEV)')

draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_equal,
                                               title='Z3_equal_feasibility',
                                               directory='combined',
                                               x_axises=x_axises,
                                               x_axis_limit=10,
                                               y1_axises=y1_axises,
                                               y2_axises=y2_axises,
                                               x_axis_label='Number of Slices',
                                               y1_axis_label='Objective (ms)',
                                               y2_axis_label='Solution Time (sec)',
                                               y1_stdevs=y1_stdevs,
                                               y2_stdevs=y2_stdevs,
                                               markers=['s'],
                                               fig_size=[10, 3.4],
                                               log_scale_y=True)

# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_equal,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_Z3_equal_feasibility_(Zoom)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=8,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
#
# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_equal,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_Z3_equal_feasibility_(Zoom +)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=2,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)


# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_scalar,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_Z3_scalar_feasibility',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y1_axis_limit=1500,
#                                                     y2_axis_limit=500,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)


# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_scalar,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_Z3_scalar_feasibility_(Zoom)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=8,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
#
# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_scalar,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_and_Z3_calar_feasibility_(Zoom +)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=2,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
#
# draw_line_graph_with_multiple_y_axis_and_files(filenames=filenames_feasible_scalar,
#                                                     title=str(solvers[0]) + '_' + str(solvers[1]) + '_Z3_scalar_feasibility_(Zoom ++)',
#                                                     directory='combined',
#                                                     x_axises=x_axises,
#                                                     y1_axises=y1_axises,
#                                                     y2_axises=y2_axises,
#                                                     x_axis_label='Number of Slices (#)',
#                                                     x_axis_limit=32,
#                                                     y1_axis_label='Objective (sec)',
#                                                     y2_axis_label='Solution Time (sec)',
#                                                     y2_axis_limit=0.5,
#                                                     y1_stdevs=y1_stdevs,
#                                                     y2_stdevs=y2_stdevs)
