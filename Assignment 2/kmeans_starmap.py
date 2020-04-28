#!/usr/bin/env python
#
# File: kmeans.py
# Author: Alexander Schliep (alexander@schlieplab.org)
#
#
import logging
import argparse
import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
import time
import multiprocessing
from functools import partial

def generateData(n, c):
    logging.info(f"Generating {n} samples in {c} classes")
    X, y = make_blobs(n_samples=n, centers = c, cluster_std=1.7, shuffle=False,
                      random_state = 2122)
    return X


def nearestCentroid(datum, centroids):
    # norm(a-b) is Euclidean distance, matrix - vector computes difference
    # for all rows of matrix
    dist = np.linalg.norm(centroids - datum, axis=1)
    return np.argmin(dist), np.min(dist)

def assignDatapointsToNearestCentroid(variation, cluster_sizes, input, output, data, c):
    N=len(data)
    if not input.empty():
        centroids=input.get()
        for i in range(N):
            cluster, dist = nearestCentroid(data[i], centroids)
            c[i] = cluster
            cluster_sizes[cluster] += 1
            variation[cluster] += dist ** 2
        output.put((c, cluster_sizes, variation))

def zeros(name):
    for i in range(len(name)):
        name[i]=0
    return name


def kmeans(k, data, nr_iter = 100, timeParallel=0):
    N = len(data)
    # Choose k random data points as centroids
    centroids = data[np.random.choice(np.array(range(N)),size=k,replace=False)]
    logging.debug("Initial centroids\n", centroids)
    Xsub = np.split(data, args.workers)
    # The cluster index: c[i] = j indicates that i-th datum is in j-th cluster
    #c = np.zeros(N, dtype=int)
    logging.info("Iteration\tVariation\tDelta Variation")
    total_variation = 0.0
    variation = np.zeros(k)
    cluster_sizes = np.zeros(k, dtype=int)

    input=multiprocessing.Queue()
    output=multiprocessing.Queue()
    pStart = time.perf_counter()
    assignDatapointsToNearestCentroid_functool=partial(assignDatapointsToNearestCentroid, variation, cluster_sizes, input, output)
    pool_tuple = [(Xsub[i], np.zeros(len(Xsub[i]))) for i in range(args.workers)]
    with multiprocessing.Pool(processes=args.workers) as pool:
        multi_result = [pool.apply_async(assignDatapointsToNearestCentroid_functool, inp) for inp in pool_tuple]
    for i in range(args.workers): # initially tell workers that they should keep sampling
        input.put(centroids)
    for j in range(nr_iter):
        logging.debug("=== Iteration %d ===" % (j+1))
             # Assign data points to nearest centroid
             #result = pool.starmap(assignDatapointsToNearestCentroid, pool_tuple) #one result
             #map only has one argument
        c=[]
        cluster_sizes=[]
        variation=[]
        for _ in range (args.workers):
            c1,cluster_sizes1,variation1= output.get()
            c+=c1
            cluster_sizes+=cluster_sizes1
            variation+=variation1
        c = np.concatenate(c)
        c = c.astype(int)

        pFinish = time.perf_counter()
        timeParallel += pFinish - pStart
        result=np.array(result).T
        for n in result[1]:
            cluster_sizes=np.add(cluster_sizes,n)
        variation=np.concatenate(result[2])
        """
        for i in range(N):
        cluster, dist = nearestCentroid(data[i],centroids)
        c[i] = cluster
        cluster_sizes[cluster] += 1
        variation[cluster] += dist**2
        """
        delta_variation = -total_variation
        total_variation = sum(variation)
        delta_variation += total_variation
        logging.info("%3d\t\t%f\t%f" % (j, total_variation, delta_variation))

        # Recompute centroids
        centroids = np.zeros((k,2)) # This fixes the dimension to 2
        for i in range(N):
           centroids[c[i]] += data[i]
        centroids = centroids / cluster_sizes.reshape(-1,1)
        
    logging.debug(cluster_sizes)
    logging.debug(c)
    logging.debug(centroids)
    
    return total_variation, c, timeParallel


def computeClustering(args):
    if args.verbose:
        logging.basicConfig(format='# %(message)s',level=logging.INFO)
    if args.debug: 
        logging.basicConfig(format='# %(message)s',level=logging.DEBUG)

    
    X = generateData(args.samples, args.classes)
    start_time = time.time()
    #
    # Modify kmeans code to use args.worker parallel threads
    total_variation, assignment, timeParallel = kmeans(args.k_clusters, X, nr_iter = args.iterations)
    #
    #
    end_time = time.time()
    logging.info("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print("Clustering complete in %3.2f [s]" % (end_time - start_time))
    print("Parallel complete in %3.2f [s]" % timeParallel)
    print("Portion of paralleled programm in %3.2f [s]" % (timeParallel/(end_time - start_time)))
    print(f"Total variation {total_variation}")

    if args.plot: # Assuming 2D data
        fig, axes = plt.subplots(nrows=1, ncols=1)
        axes.scatter(X[:, 0], X[:, 1], c=assignment, alpha=0.2)
        plt.title("k-means result")
        #plt.show()        
        fig.savefig(args.plot)
        plt.close(fig)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Compute a k-means clustering.',
        epilog = 'Example: kmeans.py -v -k 4 --samples 10000 --classes 4 --plot result.png'
    )
    parser.add_argument('--workers', '-w',
                        default='1',
                        type = int,
                        help='Number of parallel processes to use (NOT IMPLEMENTED)')
    parser.add_argument('--k_clusters', '-k',
                        default='3',
                        type = int,
                        help='Number of clusters')
    parser.add_argument('--iterations', '-i',
                        default='100',
                        type = int,
                        help='Number of iterations in k-means')
    parser.add_argument('--samples', '-s',
                        default='10000',
                        type = int,
                        help='Number of samples to generate as input')
    parser.add_argument('--classes', '-c',
                        default='3',
                        type = int,
                        help='Number of classes to generate samples from')   
    parser.add_argument('--plot', '-p',
                        default='True',
                        type = str,
                        help='Filename to plot the final result')   
    parser.add_argument('--verbose', '-v',
                        action='store_true',
                        help='Print verbose diagnostic output')
    parser.add_argument('--debug', '-d',
                        action='store_true',
                        help='Print debugging output')
    args = parser.parse_args()
    computeClustering(args)

