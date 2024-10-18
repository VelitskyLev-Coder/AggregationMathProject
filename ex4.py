import os
import numpy as np

from aggregation import aggregate


def build_ex4_example(n, n_walkers, sticky_points, distribution_type, example_name, normal_distribution=None):
    save_dir = f'target\\ex4\\example_{example_name}'
    os.makedirs(save_dir, exist_ok=True)

    grid = aggregate(n, n_walkers, save_plot_dir=save_dir,
                     save_plot_name=f'{distribution_type}_n_{n}_walkers_{n_walkers}_sticky_{len(sticky_points)}',
                     sticky_points=sticky_points, create_video=False,
                     normal_distribution=normal_distribution)


# Function to generate circular sticky points
def generate_circle_sticky_points(n, radius):
    center_x, center_y = n // 2, n // 2  # Center of the grid
    sticky_points = []

    for angle in np.linspace(0, 2 * np.pi, num=360):
        x = int(center_x + radius * np.cos(angle))
        y = int(center_y + radius * np.sin(angle))
        if 0 <= x < n and 0 <= y < n:  # Ensure points are within grid bounds
            sticky_points.append((x, y))
    return sticky_points


# Function to generate triangular sticky points
def generate_triangle_sticky_points(n, base_height_ratio=0.5):
    base_width = n // 2
    height = int(base_height_ratio * n)
    center_x, center_y = n // 2, n // 2  # Center of the grid
    sticky_points = []

    for y in range(center_y, center_y + height):
        start_x = center_x - (base_width * (y - center_y)) // height
        end_x = center_x + (base_width * (y - center_y)) // height
        for x in range(start_x, end_x + 1):
            sticky_points.append((x, y))
    return sticky_points


# Generate 10 Examples

def generate_examples():
    n = 128  # Grid size
    examples = []

    # Example 1: Uniform distribution, sticky points at n/4 row
    sticky_points = [(i, n // 4) for i in range(n)]  # Sticky particles along row n/4
    examples.append(("uniform", n, 850, sticky_points, "row_n4", None))

    # Example 2: Gaussian distribution, sticky points at n/4 row
    examples.append(("gaussian", n, 900, sticky_points, "gaussian_row_n4", 20.0))

    # Example 3: Uniform distribution, sticky points at n/2 row
    sticky_points = [(i, n // 2) for i in range(n)]  # Sticky particles along row n/2
    examples.append(("uniform", n, 1000, sticky_points, "row_n2", None))

    # Example 4: Gaussian distribution, sticky points at n/2 row
    examples.append(("gaussian", n, 1100, sticky_points, "gaussian_row_n2", 15.0))

    # Example 5: Circular sticky points with radius 20, uniform distribution
    sticky_points = generate_circle_sticky_points(n, 20)  # Circle with radius 20
    examples.append(("uniform", n, 900, sticky_points, "circle_r20", None))

    # Example 6: Circular sticky points with radius 20, Gaussian distribution
    examples.append(("gaussian", n, 950, sticky_points, "gaussian_circle_r20", 10.0))

    # Example 7: Triangular sticky points, uniform distribution
    sticky_points = generate_triangle_sticky_points(n, base_height_ratio=0.5)  # Triangle base/height = 0.5
    examples.append(("uniform", n, 800, sticky_points, "triangle_bh0.5", None))

    # Example 8: Triangular sticky points, Gaussian distribution
    examples.append(("gaussian", n, 850, sticky_points, "gaussian_triangle_bh0.5", 25.0))

    # Example 9: Circular sticky points with radius 30, uniform distribution
    sticky_points = generate_circle_sticky_points(n, 30)  # Circle with radius 30
    examples.append(("uniform", n, 1150, sticky_points, "circle_r30", None))

    # Example 10: Circular sticky points with radius 30, Gaussian distribution
    examples.append(("gaussian", n, 1200, sticky_points, "gaussian_circle_r30", 30.0))

    # Run the 10 examples
    for example in examples:
        distribution_type, n, n_walkers, sticky_points, example_name, normal_distribution = example
        build_ex4_example(n, n_walkers, sticky_points, distribution_type, example_name, normal_distribution)


def build_ex4():
    generate_examples()


if __name__ == '__main__':
    generate_examples()
