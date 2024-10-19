import os
import random

import numpy as np
from matplotlib import pyplot as plt
from video_creator import assemble_video
from enum import Enum, auto
from matplotlib.patches import RegularPolygon
from matplotlib.collections import PatchCollection


class NeighborType(Enum):
    EIGHT_NEIGHBORS = auto()
    FOUR_NEIGHBORS = auto()
    SIX_NEIGHBORS_TRIANGULAR = auto()  # New type for 6-neighbor triangular lattice


def plot_hexagonal(grid, save_plot_name=None, save_plot_dir=None, iteration=None):
    """
    Optimized version of plotting the grid with a hexagonal layout.
    Uses PolyCollection for faster drawing of hexagons.
    """
    n, _ = grid.shape
    fig, ax = plt.subplots(figsize=(8, 8))

    hex_radius = 1  # Radius of each hexagon
    x_spacing = np.sqrt(3) * hex_radius  # Horizontal distance between hexagon centers
    y_spacing = 1.5 * hex_radius  # Vertical distance between hexagon centers (staggered)

    # Precompute the x and y coordinates for even and odd rows
    hexagons = []
    colors = []

    for i in range(n):
        for j in range(n):
            # Adjust x-coordinate for staggered rows
            x = j * x_spacing
            y = i * y_spacing
            if i % 2 == 1:  # Shift odd rows
                x += x_spacing / 2

            # Set color based on grid value
            if grid[i, j] == 2:  # Sticky points
                color = 'red'
            elif grid[i, j] == 1:  # Mobile walkers
                color = 'blue'
            else:
                color = 'none'  # Empty cells will be transparent

            # Add a hexagonal patch at the (x, y) position
            hexagon = RegularPolygon((x, y), numVertices=6, radius=hex_radius * 0.95,
                                     orientation=np.radians(30))
            hexagons.append(hexagon)
            colors.append(color)

    # Create a collection of hexagons with corresponding colors
    collection = PatchCollection(hexagons, facecolor=colors, edgecolor='k', linewidth=0.5, match_original=True)
    ax.add_collection(collection)

    # Set limits for x and y to match the grid
    ax.set_xlim(-x_spacing / 2, n * x_spacing)
    ax.set_ylim(-y_spacing / 2, n * y_spacing)

    ax.set_aspect('equal')
    ax.set_axis_off()  # Hide the axes for a cleaner look

    # Save the plot if save_plot_name is provided
    if save_plot_name and save_plot_dir:
        if iteration is not None:
            # Add iteration number to filename for video frames
            save_path = f'{save_plot_dir}\\{save_plot_name}_iter_{iteration:04d}.png'
        else:
            save_path = f'{save_plot_dir}\\{save_plot_name}.png'
        ax.set_title(f'{save_plot_name}')
        fig.savefig(save_path)

    plt.close(fig)


def aggregate(n: int,
              n_walkers: int,
              max_iterations: int = None,
              save_plot_dir: str = None,
              save_plot_name: str = None,
              sticky_points: list[tuple[int, int]] = None,
              create_video: bool = False,
              normal_distribution: float = None,
              neighbor_type: NeighborType = NeighborType.EIGHT_NEIGHBORS):
    tmp_dir = ""
    if save_plot_dir is not None:
        os.makedirs(save_plot_dir, exist_ok=True)
        if create_video:
            tmp_dir = f'{save_plot_dir}/tmp_{save_plot_name}'
            os.makedirs(tmp_dir, exist_ok=True)

    # Set default movement steps for 4 and 8 neighbor types
    x_step = np.array([-1, 0, 1, 0])  # Template arrays for random walk (4-neighbors)
    y_step = np.array([0, -1, 0, 1])

    if neighbor_type == NeighborType.EIGHT_NEIGHBORS:
        dx = np.array([-1, 0, 1, 0, -1, 1, 1, -1])  # Template arrays for sticking (8 neighbors)
        dy = np.array([0, -1, 0, 1, -1, -1, 1, 1])
    elif neighbor_type == NeighborType.FOUR_NEIGHBORS:
        dx = np.array([-1, 0, 1, 0])  # Template arrays for sticking (4 neighbors)
        dy = np.array([0, -1, 0, 1])
    elif neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
        # Even/odd row dependent neighbors for triangular lattice
        dx_even = np.array([0, 1, 1, 0, -1, -1])
        dy_even = np.array([-1, -1, 0, 1, 0, -1])
        dx_odd = np.array([1, 1, 0, -1, -1, 0])
        dy_odd = np.array([1, 0, 1, 1, 0, -1])

    grid = np.zeros([n + 2, n + 2], dtype='int')  # Lattice array

    x = np.zeros(n_walkers, dtype='int')  # Walker x-coordinate in nodal unit
    y = np.zeros(n_walkers, dtype='int')  # Walker y-coordinate in nodal unit
    status = np.ones(n_walkers, dtype='int')  # Walker status array: all mobile

    # Add sticky points
    for i, j in sticky_points:
        grid[i, j] = 2  # Introduce sticky central node

    # Generate walker positions
    pos_x_y = set()
    for i in range(0, n):
        for j in range(0, n):
            if grid[i][j] == 0:
                pos_x_y.add((i, j))

    # Place walkers using normal distribution if specified, else randomly
    if normal_distribution is not None:
        center = n // 2
        for i in range(0, n_walkers):
            while True:
                # Generate normally distributed positions around center
                x[i] = int(np.random.normal(center, normal_distribution)) % n
                y[i] = int(np.random.normal(center, normal_distribution)) % n
                if (x[i], y[i]) in pos_x_y:
                    pos_x_y.remove((int(x[i]), int(y[i])))
                    grid[x[i], y[i]] = 1
                    break
    else:
        for i in range(0, n_walkers):  # Place walkers randomly
            x[i], y[i] = random.choice(tuple(pos_x_y))
            pos_x_y.remove((int(x[i]), int(y[i])))
            grid[x[i], y[i]] = 1

    # Initial plot
    if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
        plot_hexagonal(grid, save_plot_name=f'{save_plot_name}_start', save_plot_dir=save_plot_dir)
    else:
        fig, ax = plt.subplots()
        ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
        fig.savefig(f'{save_plot_dir}\\{save_plot_name}_start.png')
        plt.close(fig)

    # Counters
    iteration, n_glued = 0, 0

    if create_video:
        if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
            plot_hexagonal(grid, save_plot_name=save_plot_name, save_plot_dir=tmp_dir, iteration=0)
        else:
            fig, ax = plt.subplots()
            ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
            ax.set_title(f'{save_plot_name}')
            fig.savefig(f'{tmp_dir}\\frame_{0}.png')
            plt.close(fig)

    while ((n_glued < n_walkers)
           and (max_iterations is None or iteration < max_iterations)):
        for i in range(0, n_walkers):  # Loop over walkers
            if status[i] == 1:  # This walker is still mobile
                if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
                    # Handle triangular movement based on row (even/odd)
                    if x[i] % 2 == 0:  # Even row
                        step_direction = np.random.choice(6)
                        x_new = (x[i] + dx_even[step_direction]) % n
                        y_new = (y[i] + dy_even[step_direction]) % n
                    else:  # Odd row
                        step_direction = np.random.choice(6)
                        x_new = (x[i] + dx_odd[step_direction]) % n
                        y_new = (y[i] + dy_odd[step_direction]) % n
                else:
                    # Handle random walk for 4 and 8 neighbors
                    ii = np.random.choice([0, 1, 2, 3])  # Pick direction for 4-neighbors
                    x_new = (x[i] + x_step[ii]) % n  # New position on lattice
                    y_new = (y[i] + y_step[ii]) % n  # New position

                if grid[x_new, y_new] != 2:
                    grid[x_new, y_new] = 1  # Update lattice
                    grid[x[i], y[i]] = 0  # Move walker
                    x[i], y[i] = x_new, y_new

                if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
                    # Sticky check for triangular lattice based on even/odd rows
                    if x[i] % 2 == 0:  # Even row sticky check
                        if 2 in grid[(x[i] + dx_even[:]) % n, (y[i] + dy_even[:]) % n]:
                            grid[x[i], y[i]] = 2  # Stick the walker
                            status[i] = 2
                            n_glued += 1
                    else:  # Odd row sticky check
                        if 2 in grid[(x[i] + dx_odd[:]) % n, (y[i] + dy_odd[:]) % n]:
                            grid[x[i], y[i]] = 2  # Stick the walker
                            status[i] = 2
                            n_glued += 1
                else:
                    # Sticky check for 4 and 8 neighbors
                    if 2 in grid[(x[i] + dx[:]) % n, (y[i] + dy[:]) % n]:
                        grid[x[i], y[i]] = 2  # Stick the walker
                        status[i] = 2
                        n_glued += 1

        iteration += 1
        if create_video:
            if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
                plot_hexagonal(grid, save_plot_name=save_plot_name, save_plot_dir=tmp_dir, iteration=iteration)
            else:
                fig, ax = plt.subplots()
                ax.set_title(f'{save_plot_name}')
                ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
                fig.savefig(f'{tmp_dir}\\frame_{iteration}.png')
                plt.close(fig)

        if iteration % 100 == 0:
            print("iteration {0}, glued walkers {1}.".format(iteration, n_glued))

    # Final plot
    if neighbor_type == NeighborType.SIX_NEIGHBORS_TRIANGULAR:
        plot_hexagonal(grid, save_plot_name=f'{save_plot_name}_end', save_plot_dir=save_plot_dir)
    else:
        fig, ax = plt.subplots()
        ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
        fig.savefig(f'{save_plot_dir}\\{save_plot_name}_end.png')
        plt.close(fig)

    # Assemble video if requested
    if create_video:
        assemble_video(input_pattern=f'{tmp_dir}\\*.png',
                       output_path=f'{save_plot_dir}\\{save_plot_name}.mp4',
                       fps=60)

    return grid
