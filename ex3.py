
import numpy as np
import matplotlib.pyplot as plt

from aggregation import aggregate
from box_count import box_count


def build_ex3():
    n = 128
    ratio_values = np.linspace(0.02, 0.5, 30)
    slopes = []
    for ratio in ratio_values:
        walkers = round(n * n * ratio)
        grid = aggregate(n, walkers, save_plot_dir='target\\ex3',
                         save_plot_name=f'ratio_{ratio:0.2f}', sticky_points=[(n//2, n//2)])
        _, _, _, slope = box_count(n, grid)
        slopes.append(slope)

    fig, ax = plt.subplots(figsize=(8, 6))  # Create figure and axes
    ax.plot(ratio_values, slopes, marker='o', linestyle='-', color='b')  # Plot the data
    ax.set_title('Fractal Dimension (Slope) vs Ratio')  # Set title
    ax.set_xlabel('Ratio of Occupied Nodes')  # Set x-axis label
    ax.set_ylabel('Fractal Dimension (Slope)')  # Set y-axis label
    ax.grid(True)  # Enable grid

    # Save the figure
    fig.savefig('target/ex3/fractal_dimension_vs_ratio.png', dpi=300, bbox_inches='tight')


if __name__ == '__main__':
    build_ex3()
