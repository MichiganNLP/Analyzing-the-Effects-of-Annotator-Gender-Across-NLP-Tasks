import argparse
import os

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from src.config.plotting import COLORS
from src.config.task_names import TASK_ID_TO_NAME
from src.scripts.agreement.util import load_data, TASKS

OUTFILE_FMT = "output/agreement/combo/agreement_plot_{}.pdf"


HATCHES = {
    "F-ALL": None,
    "M-ALL": None,
    "F-ALLF": "xxxxx",
    "M-ALLM": "xxxxx",
    "F-ALLM": ".....",
    "M-ALLF": "....."
}

LEGEND = [
    mpatches.Patch(facecolor=COLORS["F"],label='Female agreement with aggregate'),
    mpatches.Patch(facecolor="white", edgecolor=COLORS["F"], hatch=HATCHES["F-ALLF"], label='Female agreement with female \naggregate'),
    mpatches.Patch(facecolor="white", edgecolor=COLORS["F"], hatch=HATCHES["F-ALLM"], label='Female agreement with male \naggregate'),
    mpatches.Patch(facecolor=COLORS["M"],label="Male agreement with aggregate"),
    mpatches.Patch(facecolor="white", edgecolor=COLORS["M"], hatch=HATCHES["M-ALLM"], label='Male agreement with male \naggregate'),
    mpatches.Patch(facecolor="white", edgecolor=COLORS["M"], hatch=HATCHES["M-ALLF"], label='Male agreement with female \naggregate'),
]

def _plot_task(task_name: str, ax: plt.axis):
    raw_data = load_data(task_name)

    # give order to ensure consistency across plots
    label_order = ["F-ALL", "F-ALLF", "F-ALLM", "M-ALL", "M-ALLM", "M-ALLF"]
    # renaming categories
    boxplot = ax.boxplot([raw_data[l] for l in label_order], labels=label_order, patch_artist=True, showfliers=False)
    # styling
    for patch, label in zip(boxplot['boxes'], label_order):
        patch.set_facecolor("white")
        if HATCHES[label] is None:
            patch.set_facecolor(COLORS[label[0]])
        else:
            patch.set(hatch=HATCHES[label], fill=False)
        patch.set_edgecolor(COLORS[label[0]])

    for median in boxplot['medians']:
        median.set_color('black')

    ax.set_title(TASK_ID_TO_NAME.get(task_name, task_name), fontsize="medium")
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)


def plot(use_median):
    assert len(TASKS) == 11, f"Expect 11 tasks. Change this code to allow {len(TASKS)} tasks."
    _, axes = plt.subplots(nrows=4, ncols=3, figsize=(7.5, 6), sharex=True)
    for task, ax in zip(TASKS, axes.flat):
        _plot_task(task, ax)

    # add legend in last grid space
    axes.flat[-1].axis("off")
    axes.flat[-1].legend(handles=LEGEND, loc="center", fontsize="small")

    plt.tight_layout()

    outfile = OUTFILE_FMT.format("with_medians" if use_median else "means_only")
    plt.savefig(outfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--use_median", action="store_true", 
        help="Use medians instead of means for MEDIAN_COMPUTED_TASKS")
    args = parser.parse_args()
    os.makedirs(os.path.split(OUTFILE_FMT)[0], exist_ok=True)
    plot(args.use_median)

if __name__ == "__main__":
    main()
