#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

''' Python script for proving satisfiability and validity of a given IEEE 802.11 network slicing problem using z3py'''

from z3 import *
from handlers.file_handler import ProblemHandler
from handlers.lambda_handler import *

import time
import json
import os

# Loading problem from file
problem_handler = ProblemHandler(problem_filename="../../problem_descriptors/slicing_problem.json")
from_slice = 1
until_slice = 65
lambda_distribution = 'equal'  # progressive, equal, other, random, or custom to keep the original problem
lamda_gap = 0.5
repeat = 10

for num_slices in range(from_slice, until_slice):
    for i in range(0, repeat):
        print('Problem slices loaded: ' + str(len(problem_handler.data['slices'])))
        print('Solving the first ' + str(num_slices) + ' slices...')
        print('Lambda distribution: ', lambda_distribution)
        print('Repeat: ', i)

        if lambda_distribution == 'progressive':
            problem_handler.lambda_s = compute_progressive_lambdas(num_slices=num_slices,
                                                                   rb_max_dequeuing_rate=problem_handler.rb_max_dequeuing_rate,
                                                                   lambda_factor=0.01,
                                                                   lambda_gap=lamda_gap)
        elif lambda_distribution == 'equal':
            problem_handler.lambda_s = compute_equal_lambdas(num_slices=num_slices,
                                                             rb_max_dequeuing_rate=problem_handler.rb_max_dequeuing_rate,
                                                             lambda_gap=lamda_gap)
        elif lambda_distribution == 'random':
            problem_handler.lambda_s = compute_random_lambdas(num_slices=num_slices,
                                                              rb_max_dequeuing_rate=problem_handler.rb_max_dequeuing_rate,
                                                              lambda_gap=lamda_gap)
        else:
            print('Lambda distribution not valid!')

        # Initialize variables
        q_s = []                        # Quantum values in slice s
        mu_s_pkt = []                   # Packet dequeuing rate in slice s
        mu_s = []                       # Dequeuing rate in slice s
        p_s = []                        # Service utilization in slice s
        l_q_s = []                      # Average number of bytes in slice s
        w_q_s = []                      # Average waiting time in in slice s
        objectives = []                 # Objective values computed
        initial_objective = 0           # Initial objective values computed (parsed)

        for i in range(num_slices):
            q_s.append(Real('q_s' + str(problem_handler.data['slices'][i]['id'])))
            mu_s_pkt.append(Real('mu_s_pkt' + str(problem_handler.data['slices'][i]['id'])))
            mu_s.append(Real('mu_s' + str(problem_handler.data['slices'][i]['id'])))
            p_s.append(Real('p_s' + str(problem_handler.data['slices'][i]['id'])))
            l_q_s.append(Real('l_q_s' + str(problem_handler.data['slices'][i]['id'])))
            w_q_s.append(Real('w_q_s' + str(problem_handler.data['slices'][i]['id'])))

        # Solver
        s = Solver()
        set_option(rational_to_decimal=True)
        set_option(precision=2)
        quantum_cons = []
        equations = []


        def add_constraints():
            for i in range(num_slices):

                # Quantum constraints upper and lower bounds
                crr_quantum_cons = q_s[i] > 0
                quantum_cons.append(crr_quantum_cons)
                s.add(crr_quantum_cons)

                crr_quantum_cons = q_s[i] <= problem_handler.avg_airtimes[i]
                quantum_cons.append(crr_quantum_cons)
                s.add(crr_quantum_cons)

                # Packet dequeuing rate function
                crr_equation = mu_s_pkt[i] == q_s[i] / problem_handler.avg_airtimes[i]
                equations.append(crr_equation)
                s.add(crr_equation)

            for i in range(num_slices):
                # Dequeuing rate function
                crr_equation = mu_s[i] == (mu_s_pkt[i] / sum(mu_s_pkt)) * problem_handler.rb_max_dequeuing_rate
                equations.append(crr_equation)
                s.add(mu_s[i] == (mu_s_pkt[i] / sum(mu_s_pkt)) * problem_handler.rb_max_dequeuing_rate)

                # Service utilization functions
                crr_equation = p_s[i] == problem_handler.lambda_s[i] / mu_s[i]
                equations.append(crr_equation)
                s.add(crr_equation)

                crr_equation = p_s[i] < 1
                equations.append(crr_equation)
                s.add(crr_equation)

                # Average service rate in the system
                crr_equation = l_q_s[i] == (p_s[i] * p_s[i]) / (1 - p_s[i])
                equations.append(crr_equation)
                s.add(crr_equation)

                # Average time of the queue
                crr_equation = w_q_s[i] == l_q_s[i] / problem_handler.lambda_s[i]
                equations.append(crr_equation)
                s.add(crr_equation)

                # Max queue delay time of the queue
                if problem_handler.qos_delay[i] is not None:
                    crr_equation = w_q_s[i] <= problem_handler.qos_delay[i]
                    equations.append(crr_equation)
                    s.add(crr_equation)


        # Add all constraints to the solver...
        add_constraints()

        print("Asserted constraints...")
        for c in s.assertions():
            print(c)

        # History of all steps done
        all_steps = {'start': {'num_slices': num_slices, 'lambda_distribution': lambda_distribution, 'time': time.time()}}

        # Checking feasibility...
        feasibility = s.check()

        # Saving into file
        all_steps['first_step'] = {'feasibility': str(feasibility), 'time': time.time()}
        all_steps['first_step']['feasibility_time_in_sec'] = all_steps['first_step']['time'] - all_steps['start']['time']

        print("Feasibility: " + str(feasibility))
        print("Statistics for the last check method...")
        print(s.statistics())

        # Traversing statistics
        for k, v in s.statistics():
            print("%s : %s" % (k, v))

        # Optimization flag
        optimize = False
        divide_and_conquer_method = False

        if str(feasibility) == 'sat':
            # Satisfiable solution, so SOLVE
            solve(equations + quantum_cons)

            all_steps['first_step']['solved_time'] = time.time()
            all_steps['first_step']['solved_time_in_sec'] = all_steps['first_step']['solved_time'] - all_steps['first_step']['time']

            # Adding the new objective to the vector
            objective_value = 0
            objective_parsed_float = 0
            for d in s.model().decls():
                if d.name().startswith('w_q_s'):
                    objective_value += s.model()[d]
                    objective_parsed_float += float(s.model()[d].as_decimal(4).replace('?', ''))  # Removing ? from RatNumRef
            initial_objective = objective_value

            solution = []
            delays = []
            for d in s.model().decls():
                if d.name().startswith('q_s'):
                    solution.append(s.model()[d].as_decimal(20))
                elif d.name().startswith('w_q_s'):
                    delays.append(s.model()[d].as_decimal(20))

            all_steps['first_step']['solution'] = solution
            all_steps['first_step']['delays'] = delays
            all_steps['first_step']['objective'] = objective_parsed_float

            # Let's optimize then...
            optimize = False

        if optimize:
            print('Trying to optimize...')
            opt = Optimize()

            for cons in quantum_cons:
                opt.add(cons)

            for eq in equations:
                opt.add(eq)

            h = opt.minimize(sum(w_q_s))
            print(opt.check())
            print(opt.lower(h))
            print(opt.model())

            optimization_status = opt.check()
            if str(optimization_status) == 'unknown':
                print('Z3 could not find the optimal solution by itself!')
                print('Trying divide and conquer method...')
                divide_and_conquer_method = True
                all_steps['optimization_step'] = {'feasibility': str(optimization_status), 'time': time.time()}

        # Trying divide and conquer method
        if divide_and_conquer_method:
            optimal = False
            new_objective = initial_objective / 2  # Half of the initial objective
            counter = 0
            epsilon = 0.001     # later to 1 or 0.001
            iterations_limit = 200
            all_steps['div_conq'] = []
            solution = []

            while not optimal:
                counter = counter + 1
                print('\nOptimizing: ' + str(counter))
                all_steps['div_conq'].append(
                    {'optimization_step': counter,
                     'start': time.time(),
                     'objective': str(new_objective)})

                # Creating a new scope...
                s.push()

                # Objective function of the system
                crr_equation = sum(w_q_s) <= new_objective
                equations.append(crr_equation)
                s.add(crr_equation)

                feasibility = s.check()
                if str(feasibility) == 'sat':
                    print("Asserted constraints...")
                    for c in s.assertions():
                        print(c)

                    # Satisfiable solution, so SOLVE
                    solve(equations + quantum_cons)

                    # Adding the new objective to the vector
                    objective_value = 0
                    for d in s.model().decls():
                        if d.name().startswith('t_s'):
                            objective_value += float(s.model()[d].as_decimal(12).replace('?', ''))  # Removing ? from RatNumRef
                            #objective_value += float(s.model()[d].as_decimal(12)[:-1])  # Removing ? from RatNumRef
                            # objective_value += s.model()[d]

                    objectives.append(objective_value)

                    if len(objectives) >= 2:
                        # If the difference between last objective and current is less than epsilon = stop
                        if (objectives[-2] - objectives[-1]) < epsilon:
                            print('Stopped because of epsilon!')
                            for d in s.model().decls():
                                if d.name().startswith('q_s'):
                                    print(s.model()[d])
                                    solution.append(s.model()[d].as_decimal(20))
                            optimal = True

                    new_objective = new_objective / 2   # Back reducing half of the current objective
                else:
                    # Unsatisfiable solution
                    print('**** UNSATISFIABLE **** ')

                    # Restoring state
                    print("Restoring state...")
                    s.pop()

                    # Removing last equation = the objective function
                    equations.pop()

                    # Adding the constraints again
                    add_constraints()

                    # Satisfiable solution, so SOLVE
                    # solve(equations + quantum_cons)

                    new_objective = new_objective + (new_objective * 0.5)   # Now move towards the current objective

                # If the number of iterations is reaches the limit = stop
                if counter == iterations_limit:
                    print('Stopped because of number of the number of interations reached the limit!')
                    optimal = True

                all_steps['div_conq'].append(
                    {'optimization_step': counter,
                     'finish': time.time(),
                     'feasibility': str(feasibility),
                     'new_objective': str(new_objective),
                     'optimal': str(optimal)})

                if optimal:
                    finish_time = time.time()
                    all_steps['finish'] = {'time': finish_time,
                                           'epsilon': epsilon,
                                           'iterations': counter,
                                           'objectives_list': objectives,
                                           'solution': solution,
                                           'optimality_in_sec': finish_time - all_steps['optimization_step']['time']}

        if 'finish' in all_steps:
            all_steps['finish']['feasibility_in_sec'] = all_steps['first_step']['time'] - all_steps['start']['time']
        else:
            all_steps['finish'] = {'infeasibility_in_sec': all_steps['first_step']['time'] - all_steps['start']['time']}

        results_file = open('results/z3_experiments.txt', "a+")
        results_file.write(json.dumps(all_steps)+"\n")
        results_file.close()

os.system('say Pedro, your Z3 theorem prover has finished!')

#print("All available options:")
#help_simplify()

#print('Tactics')
#describe_tactics()