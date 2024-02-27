from ProjectParameters import NUM_DAYS, STEPS_PER_DAY, VISUALIZE
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from World import World

if __name__ == "__main__":
    world = World()
    if VISUALIZE:
        ani = animation.FuncAnimation(world.fig, world.step, NUM_DAYS * STEPS_PER_DAY, interval=0, repeat=False)
        plt.show()
    else:
        for t in range(NUM_DAYS * STEPS_PER_DAY):
            world.step(t)