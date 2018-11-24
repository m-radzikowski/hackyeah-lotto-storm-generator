"""Calculation processor"""
from multiprocessing import Pool
from .thunder import Thunder


def calculate_in_parallel(func_, thunders_number, *args):
    pool = Pool(thunders_number)
    results = pool.map(func_(*args))
    return results


def calculate_in_queue(func_, thunders_number, *args):
    results = []
    for thunders in range(thunders_number):
        result = func_(*args)
        results.append(result)
    return results
