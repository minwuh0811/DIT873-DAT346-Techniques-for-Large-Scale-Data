import multiprocessing # See https://docs.python.org/3/library/multiprocessing.html
import argparse # See https://docs.python.org/3/library/argparse.html
import random
from math import pi, fabs
import time



def sample_pi(n,q):
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
    q.put(s)


def compute_pi(args, initial=1000):
    start = time.perf_counter()
    random.seed(1)
    error=1
    s_total=0
    n_total=0
    n=0
    timePara=0
    while error > args.accuracy:
        q = multiprocessing.JoinableQueue()
        processes=[]
        startP=time.perf_counter()
        for _ in range(args.workers):
            p = multiprocessing.Process(sample_pi(initial,q))
            p.start()
            processes.append(p)
        for process in processes:
            process.join()
        finishP=time.perf_counter()
        timePara+=(finishP-startP)
        while not q.empty():
            s_total += q.get()
        n_total+=initial*args.workers
        pi_est = (4.0 * s_total) / n_total
        error=fabs(pi-pi_est)
        n+=1
    print(f"Steps({initial}*{args.workers}*{n})\tSuccess\tPi est.\tError")
    print("%6d\t%7d\t%1.5f\t%1.5f" % (n_total, s_total, pi_est, pi-pi_est))
    finish = time.perf_counter()
    print(f'Finished total programme in {round((finish-start)*1000, 2)} microsecond(s) '
          f'Finished paralleled run in {round(timePara*1000,2)} microsecond(s)'
          f'Portion paralleled run in {round(timePara/(finish-start),2)}')


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
    args = parser.parse_args()
    cores = [1, 2, 4, 8, 16, 32]
    for j in cores:
        args.workers = j
        compute_pi(args)

