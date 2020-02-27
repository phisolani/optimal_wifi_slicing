#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

" Python script for making all graphs at once"

from graphs.lines import *

solvers = ['APOPT', 'IPOPT']  # IPOPT or APOPT
targets = ['feasibility', 'optimality']  # optimality of feasibility
lambda_distributions = ['equal', 'scalar']  # equal or scalar
APOPT_local = True  # or False

for s in solvers:
    for t in targets:
        for l in lambda_distributions:
            where = 'remote'
            if APOPT_local:
                if s == 'APOPT':
                    where = 'local'
            filename = '/Users/phisolani/Github/optimal_wifi_slicing/non_linear_optimization/gekko/results/processed_results_' + \
                       str(where) + '_' + str(s) + '_' + str(l) + '_' + str(t) + '.csv'

            title = str(l) + '_' + str(s) + '_' + str(t)
            try:
                draw_line_graph_with_multiple_y_axis(filename=filename,
                                                     title=title,
                                                     directory='individual',
                                                     x_axis='Number of Slices (#)',
                                                     y1_axis=str(s) + ' Objective (sec)',
                                                     y2_axis=str(s) + ' Solution Time (sec)',
                                                     x_axis_label='Number of Slices (#)',
                                                     y1_axis_label='Objective (sec)',
                                                     y2_axis_label='Solution Time (sec)',
                                                     y1_stdev=str(s) + ' Objective (STDEV)',
                                                     y2_stdev=str(s) + ' Solution Time (STDEV)')
            except:
                print('Results may not be there yet: ' + str(filename))

for l in lambda_distributions:
    filename = '/Users/phisolani/Github/optimal_wifi_slicing/theorem_prover/z3/results/processed_results_' + str(
        l) + '_z3.csv'
    title = str(l) + '_Z3_feasibility'
    try:
        draw_line_graph_with_multiple_y_axis(filename=filename,
                                             directory='individual',
                                             title=title,
                                             x_axis='Number of Slices (#)',
                                             y1_axis='Z3 Objective (sec)',
                                             y2_axis='Z3 Solution Time (sec)',
                                             x_axis_label='Number of Slices (#)',
                                             y1_axis_label='Objective (sec)',
                                             y2_axis_label='Solution Time (sec)',
                                             y1_stdev='Z3 Objective (STDEV)',
                                             y2_stdev='Z3 Solution Time (STDEV)')
    except:
        print('Results may not be there yet: ' + str(filename))
