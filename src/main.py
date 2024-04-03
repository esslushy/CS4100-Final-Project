from datetime import datetime
import ProjectParameters
from ProjectParameters import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from World import World
from tqdm import tqdm
from argparse import ArgumentParser
from pathlib import Path
import json

if __name__ == "__main__":
    args = ArgumentParser("Runs a Genetic Algorithm to Approximate the Iterated Prisoner's Experiment")
    args.add_argument("project", help="The name of the project to save this as.")
    args = args.parse_args()

    project = Path("../").joinpath(args.project)

    world = World(project)
    print("Starting Time =", datetime.now().strftime("%H:%M:%S"))
    if VISUALIZE:
        ani = animation.FuncAnimation(world.fig, world.step, NUM_DAYS * STEPS_PER_DAY, interval=20, repeat=False)
        if AS_MP4:
            FFwriter = animation.FFMpegWriter(fps=50)
            ani.save(project.joinpath("animation.mp4"), writer = FFwriter)
        else:
            plt.show()
    else:
        for t in tqdm(range(NUM_DAYS * STEPS_PER_DAY), leave=True):
            world.step(t)
    print("Ending Time =", datetime.now().strftime("%H:%M:%S"))
    world.get_agg_plot("Aggressiveness_Evolution.pdf")
    world.get_mem_plot("Memory_Evolution.pdf")
    world.get_hvst_plot("Harvest_Percentage_Evolution.pdf")
    world.plot_population("Total Population across Checkpoints.pdf")
    with project.joinpath("params.json").open("wt+") as f:
        json.dump({v: eval(v) for v in dir(ProjectParameters) if not v.startswith("__")}, f, indent=2)
