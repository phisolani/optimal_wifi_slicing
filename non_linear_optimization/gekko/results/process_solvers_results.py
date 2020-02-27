#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

''' Python script for parsing APOPT and IPOPT raw results'''

import csv
import statistics

base_path = '/Users/phisolani/Github/optimal_wifi_slicing/non_linear_optimization/gekko/results/'
server = 'remote'               # remote or local
solver = 'IPOPT'                # IPOPT or APOPT
lambda_distribution = 'equal'   # scalar, equal, or other
target = 'optimality'          # optimality or feasibility
from_slice = 1
until_slice = 65

results_file = open('processed_results_' + str(server) + '_' + str(solver) + '_' + str(lambda_distribution) + '_' + str(target) + '.csv', "w+")
results_file.write('Number of Slices (#), ' + str(solver) + ' Objective (ms), ' +
                   str(solver) + ' Objective (STDEV), ' +
                   str(solver) + ' Solution Time (sec), ' +
                   str(solver) + ' Solution Time (STDEV)\n')

for num_slices in range(from_slice, until_slice):
    path = str(base_path) + \
           str(server) + '/' + \
           str(solver) + '/' + \
           str(lambda_distribution) + '/' + \
           str(target) + '/' + \
           'raw_results_SOL_' + str(solver) + \
           '_SLC_' + str(num_slices) + \
           '_SER_' + str(server) + '.csv'

    with open(path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Skipping header
        next(csv_reader)
        objectives = []
        solution_times = []
        scaling_factor = 1.7  # (e.g., server is 2.5 slower than this machine)

        try:
            for row in csv_reader:
                objectives.append(float(row[2]))
                if server == 'remote':
                    solution_times.append(float(row[3]) / scaling_factor)
                else:
                    solution_times.append(float(row[3]))

            results_file.write(str(num_slices) + ',' +
                               str(statistics.mean(objectives) * 1000) + ',' +
                               str('{:f}'.format(statistics.stdev(objectives) * 1000)) + ',' +
                               str(statistics.mean(solution_times)) + ',' +
                               str('{:f}'.format(statistics.stdev(solution_times))) + '\n')
        except:
            print('No values for ' + str(num_slices) + '!')

results_file.close()
