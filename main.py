from ProjectParameters import NUM_DAYS, STEPS_PER_DAY
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from World import World

if __name__ == "__main__":
    world = World()
    ani = animation.FuncAnimation(world.fig, world.step, NUM_DAYS * STEPS_PER_DAY)
    plt.show()