'''
自定义一个 python 函数，实现 map() 函数的功能
'''


def my_map(func, seqs):
    for arg in seqs:
        yield func(arg)


def square(x):
    return x**2


new_list = my_map(square, [1, 2, 3])
print(list(new_list))