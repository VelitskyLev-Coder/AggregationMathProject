import numpy as np
from matplotlib import pyplot as plt


def box_count(n, grid, occ_val=2):
    # Input is 2D array "grid", of size nxn; value = 2 means occupied node
    n_scales = 1  # Calculate number of scales

    while (2 ** n_scales < n) and (n_scales < 100):
        n_scales += 1

    scale = np.zeros(n_scales)  # Will hold all box size values
    n_box = np.zeros(n_scales)  # Will hold the boxcount

    for iscale in range(0, n_scales):  # Loop over allowed scales
        block_size = 2 ** (iscale + 1)  # Block size for this scale
        n_block = n // block_size  # Number of blocks for this scale
        n_box[iscale] = 0

        for i in range(0, n_block):  # Loop over first dimension
            i1 = block_size * i  # i-range of this block
            i2 = block_size * (i + 1)

            for j in range(0, n_block):  # Loop over second dimension
                j1 = block_size * j  # j-range of this block
                j2 = block_size * (j + 1)

                if occ_val in grid[i1:i2, j1:j2]:  # At least 1 occupied node
                    n_box[iscale] += 1  # Increment box count

        scale[iscale] = block_size

    # Perform linear regression in log-log space to find slope
    log_scale = np.log(1.0 / scale)
    log_n_box = np.log(n_box)

    # Calculate slope (the fractal dimension) using polyfit (linear regression)
    slope, intercept = np.polyfit(log_scale, log_n_box, 1)

    ## Plot log-log graph
    #plt.scatter(1. / scale, n_box)
    #plt.xscale('log')
    #plt.yscale('log')
    #plt.title(f'Fractal Dimension Estimate: Slope = {slope:.3f}')
    #plt.show()

    return n_scales, scale, n_box, slope
