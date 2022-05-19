import os
from typing import Dict, List

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch

from src.config.data import DEMOGRAPHICS_FN_MATRIX_MAP, \
    REALIABILITY_FN_MATRIX_MAP
from src.config.distribution import DISTRIBUTION_CONFIG
from src.config.plotting import COLORS
from src.config.task_names import TASK_ID_TO_NAME


SAVE_DIR = "output/distribution/combo"


def plot_bar(raw_data: Dict[str, List[int]], ax: plt.axis, task: str):
    assert set(raw_data.keys()) == set(COLORS)
    to_concat = [pd.Series(raw_data[g], name=g).value_counts(normalize=True).mul(100) 
        for g in COLORS]
    df = pd.concat(to_concat, axis=1)
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)
    df.plot.bar(ax=ax, color=COLORS, legend=None)
    ax.set_title(TASK_ID_TO_NAME.get(task, task))
    ax.set_ylabel(None)


def plot_kde(raw_data: Dict[str, List[int]], ax: plt.axis, task: str, 
        min_score: int, max_score: int):
    assert set(raw_data.keys()) == set(COLORS)

    to_concat = [pd.Series(raw_data[g], name=g) for g in COLORS]
    df = pd.concat(to_concat, axis=1)
    df.index = df.index.astype(int)
    df.sort_index(inplace=True)
    for k in raw_data:
        sns.kdeplot(raw_data[k], ax=ax, color=COLORS[k], 
                    clip=(min_score, max_score))
    ax.set_title(TASK_ID_TO_NAME.get(task, task))
    ax.set_ylabel(None)



def load_data(task) -> Dict[str, List[float]]:
    reliability_matrix = REALIABILITY_FN_MATRIX_MAP[task]()
    demographics = DEMOGRAPHICS_FN_MATRIX_MAP[task]()
    results = {}
    for dem, users in demographics.items():
        data = reliability_matrix.loc[users]
        array = data.to_numpy().flatten()
        results[dem] = array[~np.isnan(array)].tolist()
    return results

def plot_all_bar():
    tasks_bar = [task for task, conf in DISTRIBUTION_CONFIG.items() 
        if conf["annotation_type"] == "ordinal"]
    assert len(tasks_bar) == 4, f"Expect 4 tasks. Change this code to allow {len(tasks_bar)} tasks."
    fig, axes = plt.subplots(nrows=2, ncols=2)
    # add shared axis labels https://stackoverflow.com/a/53172335
    fig.add_subplot(111, frameon=False)
    for task, ax in zip(tasks_bar, axes.flat):
        plot_bar(load_data(task), ax, task)
    plt.tick_params(labelcolor="none", which="both", top=False, bottom=False, 
        left=False, right=False)
    plt.xlabel("score")
    plt.ylabel("percentage of annotations")
    handles, labels = axes.flat[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(SAVE_DIR, "bar_distribution.pdf"))


def plot_all_density():
    tasks_density = [task for task, conf in DISTRIBUTION_CONFIG.items()
        if conf["annotation_type"] == "interval"]
    assert len(tasks_density) == 4, f"Expect 7 tasks. Change this code to allow {len(tasks_density)} tasks."
    # build figure w/ layout
    # e1  e2
    # e3  e4
    # e5  e6
    # --e7--
    fig = plt.figure(constrained_layout=True)
    gs = GridSpec(4, 2, figure=fig)
    axes = []
    for row in range(3):
        for col in range(2):
            axes.append(fig.add_subplot(gs[row, col]))
    axes.append(fig.add_subplot(gs[3, :]))

    for task, ax in zip(tasks_density, axes):
        min_score = DISTRIBUTION_CONFIG[task]["min_val"]
        max_score = DISTRIBUTION_CONFIG[task]["max_val"]
        plot_kde(load_data(task), ax, task, min_score, max_score)
    handles = [Patch(facecolor=color, label=label) 
        for label, color in COLORS.items()]
    fig.legend(handles=handles, loc="upper left")
    axes[-1].set_xlabel("score")
    plt.savefig(os.path.join(SAVE_DIR, "kde_distribution.pdf"))


def main():
    os.makedirs(SAVE_DIR, exist_ok=True)
    plot_all_bar()
    plot_all_density()



if __name__ == "__main__":
    main()
