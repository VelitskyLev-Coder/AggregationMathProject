import itertools
import os

import numpy as np
from matplotlib import pyplot as plt

from mas_radius import mas_radius


def mass_radius_line():
    n = 128
    grid = np.zeros([n + 2, n + 2], dtype='int')
    occupied_value = 2
    for i in range(n // 8, n - n // 8):
        grid[n // 2][i] = occupied_value
    radii, mas_radius_result, slope = mas_radius(grid, n,
                                                 center_x=n // 2,
                                                 center_y=n // 2,
                                                 min_radius=0,
                                                 max_radius=(n - 2 * n // 8) // 2,
                                                 samples=10,
                                                 occupied_value=occupied_value
                                                 )
    return grid, radii, mas_radius_result, slope


def mass_radius_square():
    n = 128
    grid = np.zeros([n + 2, n + 2], dtype='int')
    occupied_value = 2
    for i, j in itertools.product(range(n // 8, n - n // 8), repeat=2):
        grid[i][j] = occupied_value
    radii, mas_radius_result, slope = mas_radius(grid, n,
                                                 center_x=n // 2,
                                                 center_y=n // 2,
                                                 min_radius=0,
                                                 max_radius=(n - 2 * n // 8) // 3,
                                                 samples=10,
                                                 occupied_value=occupied_value
                                                 )
    return grid, radii, mas_radius_result, slope


def build_ex1():
    # Step 1: Get the grids and mass-radius values, including radius values for x-axis
    line_grid, radius_values_line, mass_radius_line_values, slope_line = mass_radius_line()
    square_grid, radius_values_square, mass_radius_square_values, slope_square = mass_radius_square()

    # Step 2: Plot the grids (line grid and square grid)
    fig1, axs = plt.subplots(1, 2, figsize=(12, 6))

    # Plot the line grid
    axs[0].imshow(line_grid, cmap='gray')
    axs[0].set_title("Line Grid")
    axs[0].imshow(np.where(line_grid == 2, 1, 0), cmap='Reds', alpha=0.6)  # Overlay red for value = 2

    # Plot the square grid
    axs[1].imshow(square_grid, cmap='gray')
    axs[1].set_title("Square Grid")
    axs[1].imshow(np.where(square_grid == 2, 1, 0), cmap='Reds', alpha=0.6)  # Overlay red for value = 2

    plt.tight_layout()

    # Save the grid plot
    target_dir = r'target\\ex1'
    os.makedirs(target_dir, exist_ok=True)
    plt.savefig(f'{target_dir}\\grids.png')

    # Step 3: Create a separate plot for mass-radius slopes
    # Convert values to log base 2
    log2_radius_line = np.log2(radius_values_line[1:])
    log2_mass_line = np.log2(mass_radius_line_values[1:])
    log2_radius_square = np.log2(radius_values_square[1:])
    log2_mass_square = np.log2(mass_radius_square_values[1:])

    fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Define the tick values (powers of 2)
    tick_values_base2 = [2 ** x for x in range(1, 13)]  # Powers of 2: 2, 4, 8, 16, 32, 64, etc.

    # Plot for line values (log base 2 for x and y axes)
    ax1.plot(log2_radius_line, log2_mass_line, marker='o', label='Linle Grid')
    ax1.set_title("Mass-Radius for Line Grid (Log base 2)")
    ax1.set_xlabel("Log2(Radius)")
    ax1.set_ylabel("Log2(Mass)")
    ax1.grid(True, which="both", ls="--")

    # Set custom tick labels corresponding to powers of 2
    ax1.set_xticks(np.log2(tick_values_base2))  # X-axis as log base 2
    ax1.set_yticks(np.log2(tick_values_base2))  # Y-axis as log base 2
    ax1.set_xticklabels(tick_values_base2)  # Show powers of 2 on x-axis
    ax1.set_yticklabels(tick_values_base2)  # Show powers of 2 on y-axis

    ax1.text(np.log2(2), log2_mass_line[1], f'Slope={slope_line:.2f}', color='blue')

    # Plot for square values (log base 2 for x and y axes)
    ax2.plot(log2_radius_square, log2_mass_square, marker='x', label='Square Grid')
    ax2.set_title("Mass-Radius for Square Grid (Log base 2)")
    ax2.set_xlabel("Log2(Radius)")
    ax2.set_ylabel("Log2(Mass)")
    ax2.grid(True, which="both", ls="--")

    # Set custom tick labels corresponding to powers of 2
    ax2.set_xticks(np.log2(tick_values_base2))  # X-axis as log base 2
    ax2.set_yticks(np.log2(tick_values_base2))  # Y-axis as log base 2
    ax2.set_xticklabels(tick_values_base2)  # Show powers of 2 on x-axis
    ax2.set_yticklabels(tick_values_base2)  # Show powers of 2 on y-axis

    ax2.text(np.log2(2), log2_mass_square[1], f'Slope={slope_square:.2f}', color='green')

    plt.tight_layout()

    # Save the slopes plot
    plt.savefig(f'{target_dir}\\slopes.png')

    # Show the plots
    # plt.show()


if __name__ == '__main__':
    build_ex1()
