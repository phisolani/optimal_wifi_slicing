#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

''' Python script for parsing Z3 raw results'''

import json
import statistics

base_path = '/Users/phisolani/Github/optimal_wifi_slicing/theorem_prover/z3/results/'

equal_lambda_results_file = open('processed_results_equal_z3.csv', "w+")
equal_lambda_results_file.write('Number of Slices (#), Z3 Objective (ms), Z3 Objective (STDEV), Z3 Solution Time (sec), Z3 Solution Time (STDEV)\n')

scalar_lambda_results_file = open('processed_results_scalar_z3.csv', "w+")
scalar_lambda_results_file.write('Number of Slices (#), Z3 Objective (ms), Z3 Objective (STDEV), Z3 Solution Time (sec), Z3 Solution Time (STDEV)\n')

equal = {}
scalar = {}

with open(base_path + 'z3_experiments.txt') as f:
    for line in f:
        j_content = json.loads(line)
        print(j_content)

        if j_content['start']['lambda_distribution'] == 'equal':
            if j_content['start']['num_slices'] not in equal:
                equal[j_content['start']['num_slices']] = {'objectives': [], 'solution_times': []}

            equal[j_content['start']['num_slices']]['objectives'].append(j_content['first_step']['objective'])
            equal[j_content['start']['num_slices']]['solution_times'].append(
                j_content['first_step']['solved_time_in_sec'])

        elif j_content['start']['lambda_distribution'] == 'scalar':
            if j_content['start']['num_slices'] not in scalar:
                scalar[j_content['start']['num_slices']] = {'objectives': [], 'solution_times': []}

            scalar[j_content['start']['num_slices']]['objectives'].append(j_content['first_step']['objective'])
            scalar[j_content['start']['num_slices']]['solution_times'].append(
                j_content['first_step']['solved_time_in_sec'])

        else:
            print('Other lambda distribution, not parsing...')

for num_slices in equal:
    equal_lambda_results_file.write(str(num_slices) + ',' +
                               str(statistics.mean(equal[num_slices]['objectives']) * 1000) + ',' +
                               str('{:f}'.format(statistics.stdev(equal[num_slices]['objectives']) * 1000)) + ',' +
                               str(statistics.mean(equal[num_slices]['solution_times'])) + ',' +
                               str('{:f}'.format(statistics.stdev(equal[num_slices]['solution_times']))) + '\n')

for num_slices in scalar:
    scalar_lambda_results_file.write(str(num_slices) + ',' +
                                     str(statistics.mean(scalar[num_slices]['objectives']) * 1000) + ',' +
                                     str('{:f}'.format(statistics.stdev(scalar[num_slices]['objectives']) * 1000)) + ',' +
                                     str(statistics.mean(scalar[num_slices]['solution_times'])) + ',' +
                                     str('{:f}'.format(statistics.stdev(scalar[num_slices]['solution_times']))) + '\n')

print('Equal and scalar JSONs')
print(equal)
print(scalar)

equal_lambda_results_file.close()
scalar_lambda_results_file.close()
