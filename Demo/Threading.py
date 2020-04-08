import time
import concurrent.futures
#import threading
start=time.perf_counter()

def do_something(seconds):
    print(f'Sleep {seconds} second ... ')
    time.sleep(seconds)
    #print('Done sleeping ... ')
    return 'Done sleeping ... '

with concurrent.futures.ThreadPoolExecutor() as executor:
    secs=[4,5,3,2,1]
    results=executor.map(do_something,secs)
    #for result in results:
     #   print(result)

    """
    fs=[executor.submit(do_something, sec) for sec in secs]
    for f in concurrent.futures.as_completed(fs):
        print(f.result())
    """

"""
threads=[]

for _ in range(10):
    t=threading.Thread(target=do_something, args=[1.5])
    t.start()
    threads.append(t)
for thread in threads:
    thread.join()
"""
"""
t1=threading.Thread(target=do_something)
t2=threading.Thread(target=do_something)
t1.start()
t2.start()
t1.join()
t2.join()
"""

#do_something()
#do_something()

finish=time.perf_counter()

print(f'Finished in {round(finish-start, 2)} second(s)')