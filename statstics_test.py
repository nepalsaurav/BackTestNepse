import pandas as pd
from scipy import stats
import numpy as np


def corr_coef(df1, df2):
    # Perform the Pearson correlation test
    try:
        df1 = np.nan_to_num(df1, nan=0.0, posinf=0.0, neginf=0.0)
        df2 = np.nan_to_num(df2, nan=0.0, posinf=0.0, neginf=0.0)
    except:
        pass
    corr_coeff, p_value = stats.pearsonr(df1, df2)
    return corr_coeff, p_value
