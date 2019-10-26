import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.neighbors import LocalOutlierFactor


def _density_based_sample(data: pd.DataFrame, coords: list, portion=None, size=None, seed=None):
    """down sample data based on density, to prevent overplot in dense region and decrease plotting time"""
    clf = LocalOutlierFactor(n_neighbors=20, algorithm='auto',
                             leaf_size=30, metric='minkowski',
                             p=2, metric_params=None, contamination=0.1)

    # coords should already exist in data, get them by column names list
    data_coords = data[coords]
    clf.fit(data_coords)
    # original score is negative, the larger the denser
    density_score = clf.negative_outlier_factor_
    delta = density_score.max() - density_score.min()
    # density score to probability: the denser the less probability to be picked up
    probability_score = 1 - (density_score - density_score.min()) / delta
    probability_score = np.sqrt(probability_score)
    probability_score = probability_score / probability_score.sum()

    if size is not None:
        pass
    elif portion is not None:
        size = int(data_coords.index.size * portion)
    else:
        raise ValueError('Either portion or size should be provided.')
    if seed is not None:
        np.random.seed(seed)
    selected_cell_index = np.random.choice(data_coords.index,
                                           size=size,
                                           replace=False,
                                           p=probability_score)  # choice data based on density weights

    # return the down sampled data
    return data.reindex(selected_cell_index)


def _translate_coord_name(coord_name):
    return coord_name.upper().replace('_', ' ')


def _make_tiny_axis_label(ax, x, y, arrow_kws=None, fontsize=6):
    """this function assume coord is [0, 1]"""
    # clean ax axises
    ax.set(xticks=[], yticks=[], xlabel=None, ylabel=None)
    sns.despine(ax=ax, left=True, bottom=True)

    _arrow_kws = dict(width=0.003, linewidth=0, color='black')
    if arrow_kws is not None:
        _arrow_kws.update(arrow_kws)

    ax.arrow(0.06, 0.06, 0, 0.06, **_arrow_kws)
    ax.arrow(0.06, 0.06, 0.06, 0, **_arrow_kws)
    ax.text(0.09, 0.03, _translate_coord_name(x),
            fontdict=dict(fontsize=fontsize,
                          horizontalalignment='left',
                          verticalalignment='center'))
    ax.text(0.03, 0.09, _translate_coord_name(y),
            fontdict=dict(fontsize=fontsize, rotation=90,
                          horizontalalignment='left',
                          verticalalignment='center'))
    return
