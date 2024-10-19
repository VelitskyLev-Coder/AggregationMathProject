import concurrent.futures

from ex1 import build_ex1
from ex3 import build_ex3
from ex4 import build_ex4
from ex5 import build_ex5
from ex6 import build_ex6


def run_functions_in_process_pool(functions):
    """
    Runs the given functions concurrently in a process pool.

    Parameters:
    functions (list): List of functions to execute. Each function should take no parameters.
    """
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit each function to the process pool
        futures = [executor.submit(func) for func in functions]

        # Wait for all functions to complete and retrieve their results
        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()  # This will block until the function completes
                print(f"Function completed with result: {result}")
            except Exception as e:
                print(f"Function raised an exception: {e}")


if __name__ == '__main__':
    run_functions_in_process_pool([build_ex1,
                                   build_ex3,
                                   build_ex4,
                                   build_ex5,
                                   build_ex6])
