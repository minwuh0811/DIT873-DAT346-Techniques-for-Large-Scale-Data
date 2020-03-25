import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
import time
from math import pi

def sample_pi(n):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed()
    print("Hello from a worker")
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    return s


def compute_pi(args):
    start_time = time.time()
    random.seed(1)
    n = int(args.steps / args.workers)
    
    p = multiprocessing.Pool(args.workers)
    s = p.map(sample_pi, [n]*args.workers)

    n_total = n*args.workers
    s_total = sum(s)
    pi_est = (4.0*s_total)/n_total
    timeinterval = (time.time() - start_time)*1000
    print(" Cores\tSteps\tSuccess\tPi est.\tError\t time ")
    print("%2d\%6d\t%7d\t%1.5f\t%1.5f\%5d" % (args.workers, n_total, s_total, pi_est, pi-pi_est, timeinterval ))


if __name__ == "__main__":
    ks= [1, 2, 4, 8, 16, 32]
    for k in ks :
        parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
        parser.add_argument('--workers', '-w',
                        default=k,
                        type = int,
                        help='Number of parallel processes')
        parser.add_argument('--steps', '-s',
                        default='1000',
                        type = int,
                        help='Number of steps in the Monte Carlo simulation')
        args = parser.parse_args()
        compute_pi(args)
