#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

''' Python script for solving IEEE 802.11 network slicing problem using gekko non-linear solvers'''

from gekko import GEKKO

import json
import time


class SlicingProblem:

    def __init__(self, problem_filename=None, results_filename=None):
        self.problem_filename = problem_filename
        self.results_filename = results_filename
        self.results_file = None
        self.data = {}

    def load_problem_file(self):
        if self.problem_filename is not None:
            try:
                with open(self.problem_filename) as json_file:
                    self.data = json.load(json_file)
            except FileNotFoundError as ex:
                print('Problem file not found!', ex)

    def init_results_file(self):
        if self.results_filename is not None:
            self.results_file = open(self.results_filename, "w+")

            # Writing the header of the file
            self.results_file.write("#, Objective, Time (sec)\n")

    def solve(self, num_slices=0, remote_flag=True, solver=1):
        try:
            # Initialize gekko model (server='http://xps.apmonitor.com')
            m = GEKKO(remote=remote_flag, name="optimal_wifi_slicing")  # (optional) server='http://xps.apmonitor.com'

            # Initialize Solver (1=ADOPT, 2=BPOPT, len(slices)=IPOPT)
            '''
                1- ADOPT: is generally the best when warm-starting from a prior solution or when the number of degrees of
                freedom (Number of Variables - Number of Equations) is less than 2000
        
                2- BPOPT has been found to be the best for systems biology applications.
        
                3- IPOPT is generally the best for problems with large numbers of degrees of freedom or when starting without
                a good initial guess.
            '''
            m.options.SOLVER = solver

            #m.solver_options = ['minlp_gap_tol 1.0e-2',
            #                    'minlp_maximum_iterations 10000',
            #                    'minlp_max_iter_with_int_sol 500',
            #                    'nlp_maximum_iterations 200']

            # ------- Initialize Input ------- #
            # Problem Input initialization
            rb_max_throughput = m.Const(self.data['resource_block']['max_throughput'],
                                        'rb_max_throughput')  # Resource Block max throughput
            min_quantum = m.Const(self.data['minimum_bounds']['minimum_quantum'], 'min_quantum')
            lambda_s = []
            avg_airtimes = []

            # equal lambdas
            # if num_slices > 0:
            #    equal_lambdas = 39 / num_slices
            # else:
            #    equal_lambdas = 39

            for slc in self.data['slices']:
                lambda_s.append(slc['req_throughput'])
                # lambda_s.append(equal_lambdas)
                avg_airtimes.append(slc['airtime_needed_avg'])

            print('RB Max Throughput: ' + str(rb_max_throughput.value))
            print('Sum of Lambdas_s: ' + str(sum(lambda_s)) + ' Mbps')
            print('Slices loaded: ' + str(len(self.data['slices'])))

            # Solve for x number of slices
            print('Solving for: ' + str(num_slices) + ' slices!')
            print('New sum of lambdas: ' + str(sum(lambda_s[0:num_slices])) + ' Mbps')

            # ------- Initialize variables ------- #
            q_s = []  # Quantum values on slice s
            mu_s_pkt = []  # Packet dequeuing rate on slice s
            mu_s = []  # Dequeuing rate on slice s
            p_s = []  # Service utilization on slice s
            n_s = []  # Average service rate on slice s
            t_s = []  # Average time in the system on slice s

            for i in range(num_slices):
                q_s.append(m.Var(lb=min_quantum, ub=avg_airtimes[i], name='q_s' + str(self.data['slices'][i]['id'])))
                mu_s_pkt.append(m.Intermediate(q_s[i] / avg_airtimes[i], name='mu_s_pkt_' + str(i)))

            for i in range(num_slices):
                mu_s.append(m.Intermediate((mu_s_pkt[i] / sum(mu_s_pkt)) * rb_max_throughput, name='mu_s_' + str(i)))
                p_s.append(m.Intermediate(lambda_s[i] / mu_s[i], name='p_s_' + str(i)))
                n_s.append(m.Intermediate(p_s[i] / (1 - p_s[i]), name='n_s_' + str(i)))
                t_s.append(m.Intermediate(n_s[i] / lambda_s[i], name='t_s_' + str(i)))

            # ------- End variables ------- #
            # ------- Equations ------- #
            for i in range(num_slices):
                m.Equation(mu_s[i] >= lambda_s[i])

            m.Equation(sum(mu_s) <= rb_max_throughput)

            for i in range(num_slices):
                m.Equation(p_s[i] < 1)
            # ------- End equations ------- #

            # Objectives are always minimized (maximization is possible by multiplying the objective by -1)
            obj = (sum(t_s))

            m.Obj(obj)
            #m.open_folder()
            m.solve(disp=True, debug=True)  # Solve

            for i in range(num_slices):
                print('q_s      ' + str(i) + ': ' + str(q_s[i].value))

            for i in range(num_slices):
                print('mu_s_pkt ' + str(i) + ': ' + str(mu_s_pkt[i].value))

            for i in range(num_slices):
                print('mu_s     ' + str(i) + ': ' + str(mu_s[i].value))

            for i in range(num_slices):
                print('p_s      ' + str(i) + ': ' + str(p_s[i].value))

            for i in range(num_slices):
                print('n_s      ' + str(i) + ': ' + str(n_s[i].value))

            for i in range(num_slices):
                print('t_s      ' + str(i) + ': ' + str(t_s[i].value))
        except:
            print("An exception occurred")


def main():
    problem = SlicingProblem(problem_filename="../../problem_descriptors/slicing_problem.json",
                             results_filename="results/slicing_results.csv")
    problem.init_results_file()
    problem.load_problem_file()
    print(problem.results_filename)
    problem.solve(num_slices=3)


if __name__ == "__main__": main()



#
#
# print('Objective: ' + str(m.options.objfcnval))
# print('SOLVETIME: ' + str(m.options.SOLVETIME))
# print('SOLVER STATUS: ' + str(m.options.SOLVESTATUS))
# results_file.write(str(num_slices) + ',' + str(m.options.objfcnval) + ',' + str(m.options.SOLVETIME) + '\n')
# time.sleep(5)
#
# results_file.close()