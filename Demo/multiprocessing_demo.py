#import multiprocessing
import concurrent.futures
import time



def do_something(seconds):
    print(f'Sleeping for {seconds} second')
    time.sleep(seconds)
   # print('Done sleeping ... ')
    return f'Done sleeping ... {seconds}'



if __name__ == '__main__':
    start = time.perf_counter()
    with concurrent.futures.ProcessPoolExecutor() as executor:
        secs=[5,4,3,2,1]
        results=executor.map(do_something, secs)
        for result in results:
            print(result)

        """
        results=[executor.submit(do_something,1) for _ in range(10)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())
            """
        #f1=executor.submit(do_something, 1)
        #print(f1.result())


    """
    processes=[]
    for _ in range(10):
        p= multiprocessing.Process(target=do_something, args=[1.5])
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
"""

    """    
    p1=multiprocessing.Process(target=do_something)
    p2=multiprocessing.Process(target=do_something)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
"""

#do_something()

    finish=time.perf_counter()
    print(f'Finished in {round(finish-start, 2)} second(s)')