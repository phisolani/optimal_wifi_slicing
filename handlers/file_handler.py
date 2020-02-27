#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

" Python classes to handle experiment files"

import json
import os


class ProblemHandler:

    def __init__(self, problem_filename=None):
        self.problem_filename = problem_filename
        self.data = {}
        self.min_quantum = 0
        self.rb_max_dequeuing_rate = 0
        self.lambda_s = []
        self.avg_airtimes = []
        self.qos_delay = []
        self.load_problem_file()

    def load_problem_file(self):
        if self.problem_filename is not None:
            try:
                with open(self.problem_filename) as json_file:
                    self.data = json.load(json_file)

                self.rb_max_dequeuing_rate = self.data['resource_block']['max_dequeuing_rate']  # Resource Block max dequeuing rate packets per second
                self.min_quantum = self.data['minimum_bounds']['minimum_quantum']       # Slices minimum quantum

                for slc in self.data['slices']:
                    self.lambda_s.append(slc['dequeuing_rate'])  # dequeuing rate packets per second
                    self.avg_airtimes.append(slc['airtime_needed_avg'])
                    if 'max_queue_delay' in slc:
                        if slc['max_queue_delay'] is not None:
                            self.qos_delay.append(slc['max_queue_delay']/1000)  # ms to sec
                        else:
                            self.qos_delay.append(None)

            except FileNotFoundError as ex:
                print('Problem file not found!', ex)

    def __str__(self):
        # Override to print a readable string presentation of your object
        return ', '.join(['{key}={value}'.format(key=key, value=self.__dict__.get(key)) for key in self.__dict__])


class ExperimentHandler:

    def __init__(self, results_filename=None):
        self.results_filename = results_filename
        self.results_file = None

    def init_results_file(self):
        if self.results_filename is not None:

            if os.path.exists(self.results_filename):
                append_write = 'a'
            else:
                append_write = 'w'

            self.results_file = open(self.results_filename, append_write)

            if append_write == 'w':
                # Writing the header of the file
                self.results_file.write(
                    'Experiment (#), Number of Slices (#), Objective, Solution Time (sec), Lambda (STDEV), QoS Constraints Removed\n')

    def write_results_into_file(self,
                                num_experiment=None,
                                num_slices=None,
                                objective=None,
                                solve_time=None,
                                lambdas_stdev=None,
                                qos_constraints_removed=None):

        line = str(num_experiment) + ',' + \
               str(num_slices) + ',' + \
               str(objective) + ',' + \
               str(solve_time) + ',' + \
               str(lambdas_stdev)

        if qos_constraints_removed is not None:
            line += ',' + str(qos_constraints_removed)

        line += '\n'

        # Writing results into file
        self.results_file.write(line)

    def close_results_file(self):
        self.results_file.close()
