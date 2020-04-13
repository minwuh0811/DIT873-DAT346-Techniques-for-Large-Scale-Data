import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random

from math import pi

import time as t


def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s


def compute_pi(args):
    start_time = t.time()
    random.seed(42)
    n = int(args.steps / args.workers)
    
    p = multiprocessing.Pool(args.workers)

    parallel_start_time = t.time()
    s = p.map(sample_pi, [n]*args.workers)
    parallel_total_time = 1000 * (t.time() - parallel_start_time)

    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    total_time = 1000*(t.time()-start_time)
    f =  parallel_total_time/total_time
    print("------------------------------------------")
    print(" Cores\tSteps\tSuccess\tPi est.\tError\tTOTAL time(ms)\tf=T/P est")
    print("%6d\t%6d\t%7d\t%1.5f\t%1.5f\t%1.5f\t%1.5f" % (args.workers, n_total, s_total, pi_est, pi-pi_est, total_time, f))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--steps', '-s',
                        default='1000',
                        type = int,
                        help='Number of steps in the Monte Carlo simulation')
    args = parser.parse_args()

    steps = [1, 10, 100, 1000, 10000]
    for i in steps:
        args.steps = i * 1000
        cores = [1, 2, 4, 8, 16, 32]
        for j in cores:
            args.workers = j
            compute_pi(args)


