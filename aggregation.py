import os
import random

import numpy as np
from matplotlib import pyplot as plt
from video_creator import assemble_video
from enum import Enum, auto


class NeighborType(Enum):
    EIGHT_NEIGHBORS = auto()
    FOUR_NEIGHBORS = auto()


def aggregate(n: int,
              n_walkers: int,
              max_iterations: int = None,
              save_plot_dir: str = None,
              save_plot_name: str = None,
              sticky_points: list[tuple[int, int]] = None,
              create_video: bool = False,
              normal_distribution: float = None,
              neighbor_type: NeighborType = NeighborType.EIGHT_NEIGHBORS):  # New parameter added

    tmp_dir = ""
    if save_plot_dir is not None:
        os.makedirs(save_plot_dir, exist_ok=True)
        if create_video:
            tmp_dir = f'{save_plot_dir}/tmp_{save_plot_name}'
            os.makedirs(tmp_dir, exist_ok=True)

    x_step = np.array([-1, 0, 1, 0])  # Template arrays for random walk
    y_step = np.array([0, -1, 0, 1])

    if neighbor_type == NeighborType.EIGHT_NEIGHBORS:
        dx = np.array([-1, 0, 1, 0, -1, 1, 1, -1])  # Template arrays for sticking
        dy = np.array([0, -1, 0, 1, -1, -1, 1, 1])
    elif neighbor_type == NeighborType.FOUR_NEIGHBORS:
        dx = np.array([-1, 0, 1, 0])  # Template arrays for sticking
        dy = np.array([0, -1, 0, 1])

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

    if save_plot_name:
        fig, ax = plt.subplots()
        ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
        fig.savefig(f'{save_plot_dir}\\{save_plot_name}_start.png')
        plt.close(fig)

    # Counters
    iteration, n_glued = 0, 0
    while ((n_glued < n_walkers)
           and (max_iterations is None or iteration < max_iterations)):
        for i in range(0, n_walkers):  # Loop over walkers
            if status[i] == 1:  # This walker is still mobile
                ii = np.random.choice([0, 1, 2, 3])  # Pick direction
                x_new = x[i] + x_step[ii]  # New position on lattice
                y_new = y[i] + y_step[ii]
                x_new = (n + x_new) % n  # Periodic boundaries in x
                y_new = (n + y_new) % n  # Periodic boundaries in y
                if grid[x_new, y_new] != 2:
                    grid[x_new, y_new] = 1  # Update lattice
                    grid[x[i], y[i]] = 0  # Move walker
                    x[i], y[i] = x_new, y_new
                if 2 in grid[(x[i] + dx[:]) % n, (y[i] + dy[:]) % n]:  # Check for sticky neighbor
                    grid[x[i], y[i]] = 2  # Assign sticky status to walker
                    status[i] = 2
                    n_glued += 1
        iteration += 1
        if create_video:
            fig, ax = plt.subplots()
            ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
            fig.savefig(f'{tmp_dir}\\frame_{iteration}.png')
            plt.close(fig)
        if iteration % 100 == 0:
            print("iteration {0}, glued walkers {1}.".format(iteration, n_glued))

    # Final plot
    fig, ax = plt.subplots()
    ax.imshow(grid, interpolation="nearest")  # Display aggregate as pixel image
    if save_plot_name:
        fig.savefig(f'{save_plot_dir}\\{save_plot_name}.png')

    plt.close(fig)

    if create_video:
        assemble_video(input_pattern=f'{tmp_dir}\\frame_*.png',
                       output_path=f'{save_plot_dir}\\{save_plot_name}.mp4',
                       fps=60)

    return grid
