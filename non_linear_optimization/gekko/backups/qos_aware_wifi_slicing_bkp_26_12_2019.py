#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

''' Python class for solving IEEE 802.11 network slicing problem using gekko non-linear solvers'''

from handlers.file_handler import *
from handlers.lambda_handler import *
from graphs.lines import make_graph_with_multiple_y_axis

from gekko import GEKKO
import numpy as np
import time
import os


class SlicingProblem:

    def __init__(self, name=None, remote=True, solver=1):

        # Problem name
        self.name = name

        # Initialize Gekko Model
        self.model = GEKKO(remote=remote, name=name)  # (optional) server='http://xps.apmonitor.com'

        # Initialize Solver (1=ADOPT, 2=BPOPT, len(slices)=IPOPT)
        self.model.options.SOLVER = solver

        # Additional options
        # self.model.options.IMODE = 3

        # self.model.options.MAX_ITER = 5000000

        # Initialize the number of major iterations required to find a solution
        # self.model.solver_options = ['minlp_maximum_iterations 500', \
        #                             # minlp iterations with integer solution
        #                             'minlp_max_iter_with_int_sol 10', \
        #                             # treat minlp as nlp
        #                             'minlp_as_nlp 0', \
        #                             # nlp sub-problem max iterations
        #                             'nlp_maximum_iterations 500', \
        #                             # 1 = depth first, 2 = breadth first
        #                             'minlp_branch_method 2', \
        #                             # maximum deviation from whole number
        #                             'minlp_integer_tol 20', \
        #                             # covergence tolerance
        #                            'minlp_gap_tol 20']

    def solve(self,
              num_experiment=0,
              num_slices=0,
              compute_new_lambdas_flag=False,
              lambda_distribution=None,
              qos_constraints_to_remove=None,
              problem_handler=ProblemHandler(),
              experiment_handler=ExperimentHandler(),
              objective_function=True):

        # Set this to false in case original problem lambdas wanted
        if compute_new_lambdas_flag and lambda_distribution is not None:
            if lambda_distribution == 'progressive' or lambda_distribution == 'other':
                problem_handler.lambda_s = compute_progressive_lambdas(num_slices=num_slices,
                                                                       rb_max_dequeuing_rate=problem_handler.rb_max_dequeuing_rate,
                                                                       lambda_factor=0.01,
                                                                       lambda_gap=4)
            elif lambda_distribution == 'equal':
                problem_handler.lambda_s = compute_equal_lambdas(num_slices=num_slices,
                                                                 rb_max_dequeuing_rate=problem_handler.rb_max_dequeuing_rate,
                                                                 lambda_gap=4)
            else:
                print('Lambda distribution not valid!')

        print(problem_handler)
        print('Slices to be allocated:', num_slices)
        print('SUM of the lambdas to be solved: ' + str(sum(problem_handler.lambda_s[0:num_slices])) + ' Mbps')

        # Initialize variables
        q_s = []  # Quantum values in slice s
        mu_s_pkt = []  # Packet dequeuing rate in slice s
        mu_s = []  # Dequeuing rate in slice s
        p_s = []  # Service utilization in slice s
        l_q_s = []  # Average number of bytes in slice s
        w_q_s = []  # Average waiting time in in slice s

        for i in range(num_slices):
            # Quantums
            q_s.append(self.model.Var(lb=problem_handler.min_quantum,
                                      ub=problem_handler.avg_airtimes[i],
                                      value=problem_handler.avg_airtimes[i] / 2,
                                      # Intial guess of 6000 us (12000 us / 2)
                                      name='q_s' + str(problem_handler.data['slices'][i]['id'])))

            # Packet dequeuing rate
            mu_s_pkt.append(self.model.Intermediate(q_s[i] / problem_handler.avg_airtimes[i],
                                                    name='mu_s_pkt_' + str(i)))

        for i in range(num_slices):
            # Dequeuing rate
            mu_s.append(self.model.Intermediate((mu_s_pkt[i] / sum(mu_s_pkt)) * problem_handler.rb_max_dequeuing_rate,
                                                name='mu_s_' + str(i)))

            # Service utilization
            p_s.append(self.model.Intermediate(problem_handler.lambda_s[i] / mu_s[i],
                                               name='p_s_' + str(i)))

            # Average service rate in the system
            l_q_s.append(self.model.Intermediate((p_s[i] * p_s[i]) / (1 - p_s[i]),
                                                 name='l_q_s_' + str(i)))

            # Average time of the system
            w_q_s.append(self.model.Intermediate(l_q_s[i] / problem_handler.lambda_s[i],
                                                 name='t_s_' + str(i)))

        # Equations (Constraints)
        for i in range(num_slices):
            self.model.Equation(mu_s[i] >= problem_handler.lambda_s[i])

        self.model.Equation(sum(mu_s) <= problem_handler.rb_max_dequeuing_rate)

        for i in range(num_slices):
            self.model.Equation(p_s[i] < 1)

            # Average time of the system have to be smaller than QoS delay
            if i >= qos_constraints_to_remove:
                if problem_handler.qos_delay[i] is not None:
                    self.model.Equation(w_q_s[i] <= problem_handler.qos_delay[i])

        # Objectives are always minimized (maximization is possible by multiplying the objective by -1)
        if objective_function:
            obj = (sum(w_q_s))
            self.model.Obj(obj)

        # self.model.open_folder()

        try:
            self.model.solve(disp=True, debug=True)  # Solve

            for i in range(num_slices):
                print('q_s      ' + str(i) + ': ' + str(q_s[i].value))

            for i in range(num_slices):
                print('mu_s_pkt ' + str(i) + ': ' + str(mu_s_pkt[i].value))

            for i in range(num_slices):
                print('mu_s     ' + str(i) + ': ' + str(mu_s[i].value))

            for i in range(num_slices):
                print('p_s      ' + str(i) + ': ' + str(p_s[i].value))

            for i in range(num_slices):
                print('l_q_s      ' + str(i) + ': ' + str(l_q_s[i].value))

            if not objective_function:
                sum_of_ts = 0
            for i in range(num_slices):
                print('w_q_s      ' + str(i) + ': ' + str(w_q_s[i].value))
                if not objective_function:
                    sum_of_ts += w_q_s[i].value[0]

            if not objective_function:
                objective = sum_of_ts
            else:
                objective = self.model.options.objfcnval

            print('Objective: ' + str(objective))
            print('Solve time: ' + str(self.model.options.SOLVETIME))

            experiment_handler.write_results_into_file(num_experiment=num_experiment,
                                                       num_slices=num_slices,
                                                       objective=objective,
                                                       lambdas_stdev=np.asarray(
                                                           problem_handler.lambda_s[0:num_slices]).std(),
                                                       solve_time=self.model.options.SOLVETIME,
                                                       qos_constraints_removed=qos_constraints_to_remove)
            return True
        except:
            print("An exception occurred during problem solving!")
            return False
            # from gekko.apm import get_file
            # print(self.model._server)
            # print(self.model._model_name)
            # f = get_file(self.model._server, self.model._model_name, 'infeasibilities.txt')
            # f = f.decode().replace('\r', '')
            # with open('infeasibilities.txt', 'w') as fl:
            #     fl.write(str(f))


def main():
    """
        Experiment Options
    """
    # Experiment flag
    experiment = True

    # Plot results flag
    plot_results = False

    '''
        1- ADOPT: is generally the best when warm-starting from a prior solution or when the number of degrees of
        freedom (Number of Variables - Number of Equations) is less than 2000

        2- BPOPT has been found to be the best for systems biology applications.

        3- IPOPT is generally the best for problems with large numbers of degrees of freedom or when starting without
        a good initial guess.
    '''
    solver = 1
    remote = False
    objective_function_flag = True  # True or False in case feasibility want to be computed

    if objective_function_flag:
        target = 'optimality'
    else:
        target = 'feasibility'

    if remote:
        server = 'remote'
    else:
        server = 'local'

    if solver == 1:
        solver_name = "APOPT"
    elif solver == 3:
        solver_name = "IPOPT"
    else:
        solver_name = "ALL"

    """
    Lambda distributions:
        progressive:    progressive lambda distribution
        equal:          all lambdas are equal
        other:          eliminate qos constraints one by one
        custom:         keep the original problem descriptor
    """
    lambda_distribution = 'equal'  # progressive, equal or other else to keep the original problem

    sleep = 1
    from_slice = 1
    until_slice = 65  # Set until desired slice number + 1
    repeat = 1

    # Load problem data and initialize results file
    problem_handler = ProblemHandler(problem_filename="../../problem_descriptors/slicing_problem.json")

    if experiment:
        for num_slices in range(from_slice, until_slice):

            qos_constraints_to_remove = 0  # Starts with 0, 1, 2,..

            experiment_handler = ExperimentHandler(
                results_filename='results/' + str(server) + '/' + str(solver_name) + '/' + str(lambda_distribution) +
                                 '/' + str(target) +
                                 '/raw_results_SOL_' + str(solver_name) +
                                 '_SLC_' + str(num_slices) +
                                 '_SER_' + str(server) + '.csv')

            # Init results file
            experiment_handler.init_results_file()

            for num_experiment in range(repeat):
                # Initialize problem
                problem = SlicingProblem(name="Optimal WiFi Slicing",
                                         remote=remote,
                                         solver=solver)

                if lambda_distribution == 'other':
                    # Solve the problem with all QoS constraints until 0
                    while not problem.solve(num_experiment=num_experiment,
                                            num_slices=num_slices,
                                            compute_new_lambdas_flag=True,
                                            lambda_distribution=lambda_distribution,
                                            qos_constraints_to_remove=qos_constraints_to_remove,
                                            problem_handler=problem_handler,
                                            experiment_handler=experiment_handler,
                                            objective_function=objective_function_flag):
                        print('Solve failed for ' + str(num_slices) + ' with ' + str(qos_constraints_to_remove) + '!')

                        qos_constraints_to_remove += 1

                        # unfeasible...
                        if qos_constraints_to_remove > num_slices:
                            break

                        # Reinitialise the problem
                        problem = SlicingProblem(name="Optimal WiFi Slicing",
                                                 remote=remote,
                                                 solver=solver)

                        print('Lets try with' + str(qos_constraints_to_remove) + ' constraints now!')

                else:
                    # Just solve the problem
                    if not problem.solve(num_experiment=num_experiment,
                                         num_slices=num_slices,
                                         compute_new_lambdas_flag=True,
                                         lambda_distribution=lambda_distribution,
                                         qos_constraints_to_remove=qos_constraints_to_remove,
                                         problem_handler=problem_handler,
                                         experiment_handler=experiment_handler,
                                         objective_function=objective_function_flag):
                        break
                time.sleep(sleep)

            # Close results file
            experiment_handler.close_results_file()
    os.system('say Pedro, your wifi experiment has finished!')

    if plot_results:
        for num_slices in range(from_slice, until_slice):
            make_graph_with_multiple_y_axis(filename='results/' + str(server) + '/' + str(solver_name) + '/' +
                                                     str(lambda_distribution) + '/' + str(target) +
                                                     '/raw_results_SOL_' + str(solver_name) +
                                                     '_SLC_' + str(num_slices) +
                                                     '_SER_' + str(server) + '.csv',
                                            title='Optimal WiFi Slicing (Remote=' +
                                                  str(remote) + ', Solver=' + str(solver_name) +
                                                  ', Num Slices=' + str(num_slices) + ')',
                                            x_axis='Experiment (#)',
                                            y1_axis='Objective',
                                            y2_axis='Solution Time (sec)')


if __name__ == "__main__": main()
