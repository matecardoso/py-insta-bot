import time

def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print("___________________")
        print(f"Tempo de execução ({func.__name__}): {execution_time:.2f} segundos")
        return result
    return wrapper
