import matplotlib.pyplot as plt

from aggregation import aggregate, NeighborType
from mas_radius import mas_radius


def build_ex6():
    n = 128
    slopes = []
    for i in range(3):
        grid = aggregate(n, 1000,
                         save_plot_dir=f'target\\ex6\\example_{i}',
                         save_plot_name=f'six_n',
                         sticky_points=[(n // 2, n // 2)],
                         neighbor_type=NeighborType.SIX_NEIGHBORS_TRIANGULAR,
                         create_video=True)
        plt.imshow(grid)
        plt.show()
        _, _, slope = mas_radius(grid, n,
                                 center_x=n // 2,
                                 center_y=n // 2,
                                 min_radius=0,
                                 max_radius=(n // 3) // 2,
                                 samples=10,
                                 occupied_value=2)
        slopes.append(slope)

    with open(f'target\\ex6\\slope.txt', 'w') as f:
        for value in slopes:
            f.write(f'slope={value:.2f}\n')


if __name__ == '__main__':
    build_ex6()
