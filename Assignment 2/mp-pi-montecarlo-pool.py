import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
from math import pi, fabs
import time
from functools import partial



def sample_pi(n,q,seed):
    """ Perform n steps of Monte Carlo simulation for estimating Pi/4.
        Returns the number of sucesses."""
    random.seed(seed)
    #print("Hello from a worker")
    s = 0
    for i in range(n):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1.0:
            s += 1
    q.put(s)



def compute_pi(args):
    start = time.perf_counter()
    m = multiprocessing.Manager()
    q=m.Queue()
    random.seed(1)
    error=1
    s_total=0
    n_total=0
    n=0
    sample_pi_partial = partial(sample_pi, args.steps, q)
    seeds=[]
    startP = time.perf_counter()
    with multiprocessing.Pool(processes=args.workers) as pool:
        while error > args.accuracy:
            seed = [int(random.random() * 100) for _ in range(args.workers)]
            seeds.append(seed)
            pool.map(sample_pi_partial, seed)
            for _ in range(args.workers):
                s_total += q.get()
            finishP=time.perf_counter()
            n_total+=args.steps*args.workers
            pi_est = (4.0 * s_total) / n_total
            #print(pi_est)
            error=fabs(pi-pi_est)
            n+=1
    print(f"Steps({args.steps}*{args.workers}*{n})\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, error))
    finish = time.perf_counter()
    timePara=finishP-startP
    print(f'Finished total programme in {round((finish-start)*1000, 2)} microsecond(s) '
          f'Finished paralleled run in {round(timePara*1000,2)} microsecond(s)'
          f'Portion paralleled run in {round(timePara/(finish-start),2)}')
    print(seeds)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute Pi using Monte Carlo simulation.')
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes')
    parser.add_argument('--accuracy', '-a',
                        default='10E-5',
                        type = float,
                        help='accuracy in the Monte Carlo simulation')
    parser.add_argument('--steps', '-s',
                        default='1000',
                        type = int,
                        help='Number of steps in the Monte Carlo simulation')
    args = parser.parse_args()
    #compute_pi(args)
    cores = [1, 2, 4, 8, 16, 32]
    for j in cores:
        args.workers = j
        compute_pi(args)

