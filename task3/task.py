import pandas as pd
import numpy as np
import sys
from math import log2

def task(file_path):
    existensial_matrix = pd.read_csv(file_path, header=None)
    n = existensial_matrix.shape[0]

    entropy = 0
    for l in np.array(existensial_matrix).flatten():
        w = l/(n-1)
        entropy -= 0 if w == 0 else w*log2(w)

    return round(entropy, 1)