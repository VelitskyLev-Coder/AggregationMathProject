import itertools
import math

import numpy as np


def iterate_with_step_integers(x1: int, x2: int, n: int) -> list[int]:
    total_range = x2 - x1
    base_step = total_range // (n - 1)
    remainder = total_range % (n - 1)

    result = []
    current_value = x1

    for i in range(n):
        result.append(current_value)
        # Distribute the remainder across the first few steps
        if i < remainder:
            current_value += base_step + 1
        else:
            current_value += base_step

    return result


def mas_radius(grid: np.array,
               n: int,
               center_x: int,
               center_y: int,
               min_radius: int,
               max_radius: int,
               samples: int,
               occupied_value: int) -> tuple[list[int], list[int], float]:
    result = []
    radii = iterate_with_step_integers(min_radius, max_radius, samples)

    # Calculate the mass for each radius
    for radius in radii:
        counter = 0
        for x, y in itertools.product(range(0, n), repeat=2):
            if grid[x][y] != occupied_value:
                continue
            cur_range = math.sqrt((center_x - x) ** 2 + (center_y - y) ** 2)
            if cur_range < radius:
                counter += 1
        result.append(counter)

    # Remove the first value for both radii and result to calculate slope
    log2_radii = np.log2(radii[1:])
    log2_result = np.log2(result[1:])

    # Perform linear regression to calculate the slope
    slope, _ = np.polyfit(log2_radii, log2_result, 1)

    # Return radii, result, and the calculated slope
    return radii, result, slope
