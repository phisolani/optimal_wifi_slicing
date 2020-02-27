#!/usr/bin/env python
__author__ = "Pedro Heleno Isolani"
__copyright__ = "Copyright 2019, QoS-aware WiFi Slicing"
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Pedro Heleno Isolani"
__email__ = "pedro.isolani@uantwerpen.be"
__status__ = "Prototype"

" Python functions to compute new lambdas"

import random as r


def compute_progressive_lambdas(num_slices=0, rb_max_dequeuing_rate=None, lambda_factor=0.01, lambda_gap=0.1):
    if rb_max_dequeuing_rate is not None:
        new_lambdas = []
        crr_lambda = 0
        gap_dequeuing_rate = rb_max_dequeuing_rate * lambda_gap
        for i in range(num_slices):
            if i == (num_slices - 1):
                # Last one
                new_lambdas.append(round(rb_max_dequeuing_rate - gap_dequeuing_rate - sum(new_lambdas), 2))
            else:
                crr_lambda += lambda_factor
                new_lambdas.append(round(crr_lambda, 2))
    print_new_lambdas(new_lambdas)
    return new_lambdas


def compute_equal_lambdas(num_slices=0, rb_max_dequeuing_rate=None, lambda_gap=0.1):
    if rb_max_dequeuing_rate is not None:
        new_lambdas = []
        gap_dequeuing_rate = rb_max_dequeuing_rate * lambda_gap
        new_lambda = (rb_max_dequeuing_rate - gap_dequeuing_rate) / num_slices
        for i in range(num_slices):
            new_lambdas.append(new_lambda)
    print_new_lambdas(new_lambdas)
    return new_lambdas


def compute_random_lambdas(rb_max_dequeuing_rate=None, num_slices=0, lambda_gap=0.1):
    if rb_max_dequeuing_rate is not None:
        gap_dequeuing_rate = rb_max_dequeuing_rate * lambda_gap
        rb_max_dequeuing_rate = int(rb_max_dequeuing_rate - gap_dequeuing_rate)
        num_slices = (num_slices or r.randint(2, rb_max_dequeuing_rate)) - 1
        a = r.sample(range(1, rb_max_dequeuing_rate), num_slices) + [0, rb_max_dequeuing_rate]
        list.sort(a)
        new_lambdas = [a[i+1] - a[i] for i in range(len(a) - 1)]
        print_new_lambdas(new_lambdas)
    return new_lambdas


def print_new_lambdas(new_lambdas):
    print('New lambdas: ', new_lambdas)
    print('New lambdas SUM: ', sum(new_lambdas))
