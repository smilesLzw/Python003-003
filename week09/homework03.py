'''
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数。
'''

import time
import functools


def timer(func):
    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        time_start = time.perf_counter()
        res = func(*args, **kwargs)
        time_end = time.perf_counter()
        time_spend = time_start - time_end
        print(f'{func.__name__} took {time_spend * 1000} ms')
        return res

    return func_wrapper


@timer
def func(x, y):
    return x**y


func(4, 2)
