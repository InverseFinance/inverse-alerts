import time
from concurrent.futures import ThreadPoolExecutor


def print_number(number, seconds=1):
    while True:
        print('Start %s' % number)
        time.sleep(seconds)
        print('Stop %s' % number)



if __name__ == '__main__':
    pool = ThreadPoolExecutor()
    with pool:
        x = 0
        while True:
            pool.map(print_number, x-1, 1)
            x+=1