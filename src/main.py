from ProjectParameters import NUM_DAYS, STEPS_PER_DAY, VISUALIZE
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from World import World
from tqdm import tqdm

if __name__ == "__main__":
    world = World()
    if VISUALIZE:
        ani = animation.FuncAnimation(world.fig, world.step, NUM_DAYS * STEPS_PER_DAY, interval=0, repeat=False)
        plt.show()
    else:
        for t in tqdm(range(NUM_DAYS * STEPS_PER_DAY), leave=True):
            world.step(t)
        world.get_agg_plot("Aggressiveness_Evolution.png")
        world.get_mem_plot("Memory_Evolution.png")
        world.get_hvst_plot("Harvest_Percentage_Evolution.png")