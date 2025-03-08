import time


def time_it(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time
        print(f"⏱️ Time taken: {elapsed_time:.2f} seconds")
        return result, elapsed_time

    return wrapper
