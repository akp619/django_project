#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Studybud.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()




# import time
#
# def calc_func_exe_time(function):
#     def wrapper(*args, **kargs):
#         print(kargs, "==kargs==", args, "==args==")
#         start_time = time.perf_counter()
#         result = function(*args,*kargs)
#         print("==result==", result)
#         end_time = time.perf_counter()
#         print("==start_time==", start_time, "==end_time==", end_time, result)
#         return result
#     return wrapper
#
# @calc_func_exe_time
# def demo_func(a,b):
#     print("hello world!")
#     return a*b
#
# print(demo_func(100,200))






# def get_the_data_type(data_type):
#     def convert_func_return_value(function):
#         def wrapper(*args, **kwargs):
#             print("hello!")
#             if args:
#                 print(args, "==args==", type(args))
#                 lst = list(args)
#                 print(args, "==args==2", type(args))
#             elif kwargs:
#                 print(kwargs, "==kwargs==")
#             res = function(lst, **kwargs)
#             return data_type(res)
#         print("==wrapper==", wrapper)
#         return wrapper         # calculate_values(arguements, kwargs)
#     print("==convert_func_return_value==", convert_func_return_value)
#     return convert_func_return_value    # convert_func_return_value(calculate_values)
#
#
# # convert every datatype to list
# # @get_the_data_type(int)
# def calculate_values(*args):
#     sum = 0
#     for i in args[0]:
#        sum += i**2
#     return sum
#
#
# calculate_values = get_the_data_type(int)(calculate_values)
# print(calculate_values)
# # cal_2 = calculate_values(2,3,4,5,6)
#


# new = convert_func_return_value(calculate_values)
# print(new(234567890), "==new==")

# print(calculate_values(1,2,3,4,5,6,6372,278,6736,63), type(calculate_values(1,2,3,4,5,6,6372,278,6736,63)))




# store in cache calculate time if catched and if not catched

# import time
#
# def store_in_cache(function):
#     cache = {}
#     def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         print("wrapper_called")
#         if args:
#             val = args[0]*args[1]
#             if val not in list(cache.keys()):
#                 print("value not catched")
#                 result = function(*args, **kwargs)
#                 cache[result] = args
#                 end = time.perf_counter()
#                 print("time:1", end-start)
#                 return result
#             else:
#                 print("value in cache")
#                 end = time.perf_counter()
#                 print("time:2", end - start)
#                 return val
#     return wrapper
#
# @store_in_cache
# def calculate_values(x,y):
#     print("function called for to store in cache")
#     return x*y
#
#
# print(calculate_values(2,3))
# print("=========================")
# print("=========================")
# print(calculate_values(5,6))
# print("=========================")
# print("=========================")
# print(calculate_values(5,6))
# print("=========================")
# print("=========================")



def get_the_data_type(data_type):
    def convert_func_return_value(function):
        def wrapper(*args, **kwargs):
            print(args, "==args==")
            if args:
                if data_type in [int, str]:
                    for i in args:
                        if not isinstance(i, data_type):
                            raise TypeError('Type must be %s' % data_type)
                elif data_type in [list, dict, tuple]:
                    if type(args) == data_type:
                        raise TypeError('Type must be %s' % data_type)
            return function(*args, **kwargs)
        return wrapper         # calculate_values(arguements, kwargs)
    return convert_func_return_value    # convert_func_return_value(calculate_values)


# convert every datatype to list
@get_the_data_type(int)
def calculate_integer(*args):
    sum = 0
    for i in args:
       sum += i**2
    return sum


@get_the_data_type(str)
def concatnate_values(*args):
    value = ''
    for i in args:
       value += i
    return value

@get_the_data_type(str)
def concatnate_values(*args):
    value = ''
    for i in args:
       value += i
    return value


print(calculate_integer(1,2,3,4,5))
print(concatnate_values('1','2','3','4','5'))